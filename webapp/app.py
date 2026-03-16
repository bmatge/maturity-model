"""
Webapp de suivi de maturité numérique — multi-référentiel (organisations + sites).
Flask + SQLite + DSFR + DSFR Chart
"""

import os
import json
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, ReferentielVersion, Dimension, Capacite, NiveauCritere
from models import Entite, Site, Campagne, Evaluation, Score
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(24))
db_path = os.environ.get("DATABASE_PATH", os.path.join(os.path.abspath(os.path.dirname(__file__)), "maturity.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ──────────────────────────────────────────────
# Initialisation
# ──────────────────────────────────────────────

def migrate_db():
    """Migrations incrémentales pour SQLite."""
    conn = db.engine.connect()

    # Migration 1 : ajouter referentiel_id à evaluation si absent
    eval_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(evaluation)"))]
    if "referentiel_id" not in eval_cols:
        conn.execute(text(
            "ALTER TABLE evaluation ADD COLUMN referentiel_id INTEGER REFERENCES referentiel_version(id)"
        ))
        conn.execute(text(
            "UPDATE evaluation SET referentiel_id = ("
            "  SELECT referentiel_id FROM campagne WHERE campagne.id = evaluation.campagne_id"
            ") WHERE referentiel_id IS NULL"
        ))
        conn.commit()

    # Migration 2 : supprimer referentiel_id et cible de campagne
    # SQLite ne supporte pas DROP COLUMN — on recrée la table
    camp_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(campagne)"))]
    if "referentiel_id" in camp_cols:
        conn.execute(text("CREATE TABLE campagne_new (id INTEGER PRIMARY KEY, label VARCHAR(100) NOT NULL, date_debut DATE NOT NULL, date_fin DATE, statut VARCHAR(20) DEFAULT 'en_cours')"))
        conn.execute(text("INSERT INTO campagne_new (id, label, date_debut, date_fin, statut) SELECT id, label, date_debut, date_fin, statut FROM campagne"))
        conn.execute(text("DROP TABLE campagne"))
        conn.execute(text("ALTER TABLE campagne_new RENAME TO campagne"))
        conn.commit()

    # Migration 3 : rendre campagne_id nullable sur evaluation
    # SQLite ne supporte pas ALTER COLUMN — on recrée la table
    eval_info = list(conn.execute(text("PRAGMA table_info(evaluation)")))
    campagne_col = [row for row in eval_info if row[1] == "campagne_id"]
    if campagne_col and campagne_col[0][3] == 1:  # notnull == 1
        conn.execute(text(
            "CREATE TABLE evaluation_new ("
            "id INTEGER PRIMARY KEY, referentiel_id INTEGER NOT NULL REFERENCES referentiel_version(id), "
            "campagne_id INTEGER REFERENCES campagne(id), "
            "entite_id INTEGER REFERENCES entite(id), site_id INTEGER REFERENCES site(id), "
            "evaluateur VARCHAR(200), date_evaluation DATETIME, statut VARCHAR(20) DEFAULT 'brouillon', "
            "commentaire_global TEXT)"
        ))
        conn.execute(text(
            "INSERT INTO evaluation_new (id, referentiel_id, campagne_id, entite_id, site_id, evaluateur, date_evaluation, statut, commentaire_global) "
            "SELECT id, referentiel_id, campagne_id, entite_id, site_id, evaluateur, date_evaluation, statut, commentaire_global FROM evaluation"
        ))
        # Migrer les scores (FK vers evaluation)
        conn.execute(text("DROP TABLE evaluation"))
        conn.execute(text("ALTER TABLE evaluation_new RENAME TO evaluation"))
        conn.commit()

    conn.close()


@app.before_request
def ensure_db():
    """Crée les tables et seed au premier appel."""
    if not getattr(app, "_db_ready", False):
        db.create_all()
        migrate_db()
        from seed import seed_referentiel, seed_demo_entites, seed_mini_referentiels, seed_demo_sites
        seed_referentiel()
        seed_mini_referentiels()
        seed_demo_entites()
        seed_demo_sites()
        app._db_ready = True


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def get_active_referentiel():
    return ReferentielVersion.query.filter_by(is_active=True).first()


def get_max_niveau(ref):
    """Retourne le nombre max de niveaux pour un référentiel (3 ou 4)."""
    first_cap = None
    for dim in ref.dimensions:
        if dim.capacites:
            first_cap = dim.capacites[0]
            break
    if first_cap and first_cap.niveaux:
        return max(n.niveau for n in first_cap.niveaux)
    return 4


def compute_scores_by_dimension(evaluation):
    """Retourne {dimension_id: {nom, moyenne, nb_capacites, scores_detail}}."""
    result = {}
    for score in evaluation.scores:
        cap = score.capacite
        dim = cap.dimension
        if dim.id not in result:
            result[dim.id] = {
                "nom": dim.nom,
                "numero": dim.numero,
                "scores": [],
            }
        result[dim.id]["scores"].append(score.niveau)

    for dim_id, data in result.items():
        data["moyenne"] = round(sum(data["scores"]) / len(data["scores"]), 2)
        data["nb_capacites"] = len(data["scores"])

    return dict(sorted(result.items(), key=lambda x: x[1]["numero"]))


def compute_global_stats(campagne):
    """Calcule les stats globales (moyenne, écart-type) pour une campagne."""
    evaluations = Evaluation.query.filter_by(
        campagne_id=campagne.id, statut="validee"
    ).all()

    if not evaluations:
        return None

    # Utiliser le référentiel de la première évaluation validée
    ref = evaluations[0].referentiel
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    stats = {}
    for dim in dimensions:
        dim_scores = []
        for ev in evaluations:
            scores = [s.niveau for s in ev.scores if s.capacite.dimension_id == dim.id]
            if scores:
                dim_scores.append(sum(scores) / len(scores))

        if dim_scores:
            mean = sum(dim_scores) / len(dim_scores)
            variance = sum((x - mean) ** 2 for x in dim_scores) / len(dim_scores)
            stats[dim.id] = {
                "nom": dim.nom,
                "numero": dim.numero,
                "moyenne": round(mean, 2),
                "ecart_type": round(variance ** 0.5, 2),
                "min": round(min(dim_scores), 2),
                "max": round(max(dim_scores), 2),
                "nb_entites": len(dim_scores),
            }

    return stats


# ──────────────────────────────────────────────
# Routes — Dashboard
# ──────────────────────────────────────────────

@app.route("/")
def index():
    campagnes = Campagne.query.order_by(Campagne.date_debut.desc()).all()
    entites = Entite.query.order_by(Entite.nom).all()

    # Données graphiques dashboard (scoped aux évaluations d'organisations)
    ref = get_active_referentiel()
    if not ref:
        ref = ReferentielVersion.query.first()

    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all() if ref else []
    dim_labels = [f"{d.numero}. {d.nom}" for d in dimensions]

    # Radar global : moyenne par dimension (évaluations validées d'organisations)
    all_validated = Evaluation.query.filter(
        Evaluation.statut == "validee",
        Evaluation.entite_id.isnot(None),
    ).all()
    dim_totals = {}
    for ev in all_validated:
        dim_scores = compute_scores_by_dimension(ev)
        for d in dim_scores.values():
            dim_totals.setdefault(d["numero"], []).append(d["moyenne"])

    has_charts = bool(dim_totals)
    if has_charts:
        radar_y_vals = [
            round(sum(dim_totals.get(d.numero, [0])) / max(len(dim_totals.get(d.numero, [0])), 1), 2)
            for d in dimensions
        ]
        radar_x = json.dumps([dim_labels])
        radar_y = json.dumps([radar_y_vals])
    else:
        radar_x = json.dumps([])
        radar_y = json.dumps([])

    # Bar chart : score moyen par entité (dernière évaluation validée)
    bar_labels = []
    bar_values = []
    for e in entites:
        last_ev = Evaluation.query.filter_by(entite_id=e.id, statut="validee") \
            .order_by(Evaluation.date_evaluation.desc()).first()
        if last_ev:
            dim_scores = compute_scores_by_dimension(last_ev)
            moyennes = [d["moyenne"] for d in dim_scores.values()]
            bar_labels.append(e.nom)
            bar_values.append(round(sum(moyennes) / len(moyennes), 2) if moyennes else 0)

    bar_x = json.dumps([bar_labels])
    bar_y = json.dumps([bar_values])

    # Stats pour le dashboard
    nb_referentiels = ReferentielVersion.query.count()
    nb_sites = Site.query.count()

    return render_template("index.html",
        campagnes=campagnes, entites=entites,
        radar_x=radar_x, radar_y=radar_y,
        bar_x=bar_x, bar_y=bar_y,
        has_charts=has_charts,
        nb_referentiels=nb_referentiels,
        nb_sites=nb_sites,
    )


# ──────────────────────────────────────────────
# Routes — Référentiel
# ──────────────────────────────────────────────

@app.route("/referentiel")
def referentiel_view():
    """Affiche le référentiel complet avec accordéons, recherche et filtres."""
    ref_id = request.args.get("ref_id", type=int)
    if ref_id:
        ref = ReferentielVersion.query.get_or_404(ref_id)
    else:
        ref = get_active_referentiel() or ReferentielVersion.query.first()

    all_refs = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    # Score moyen par capacité (évaluations validées de CE référentiel)
    all_validated = Evaluation.query.filter_by(
        statut="validee", referentiel_id=ref.id
    ).all()
    cap_avg = {}
    cap_counts = {}
    for ev in all_validated:
        for s in ev.scores:
            cap_avg[s.capacite_id] = cap_avg.get(s.capacite_id, 0) + s.niveau
            cap_counts[s.capacite_id] = cap_counts.get(s.capacite_id, 0) + 1

    cap_averages = {
        cid: round(total / cap_counts[cid], 1)
        for cid, total in cap_avg.items()
    }

    nb_capacites = sum(len(d.capacites) for d in dimensions)
    max_niveau = get_max_niveau(ref)

    return render_template("referentiel.html",
        referentiel=ref,
        dimensions=dimensions,
        cap_averages=cap_averages,
        nb_evaluations=len(all_validated),
        nb_capacites=nb_capacites,
        all_refs=all_refs,
        current_ref_id=ref.id,
        max_niveau=max_niveau,
    )


# ──────────────────────────────────────────────
# Routes — Entités
# ──────────────────────────────────────────────

@app.route("/entites")
def entites_list():
    entites = Entite.query.order_by(Entite.nom).all()
    return render_template("entites.html", entites=entites)


@app.route("/entites/new", methods=["GET", "POST"])
def entite_new():
    if request.method == "POST":
        entite = Entite(
            nom=request.form["nom"],
            type=request.form["type"],
            direction=request.form.get("direction", ""),
            description=request.form.get("description", ""),
        )
        db.session.add(entite)
        db.session.commit()
        flash(f"Entité « {entite.nom} » créée.", "success")
        return redirect(url_for("entites_list"))
    return render_template("entite_form.html", entite=None)


@app.route("/entites/<int:entite_id>/delete", methods=["POST"])
def entite_delete(entite_id):
    entite = Entite.query.get_or_404(entite_id)
    nom = entite.nom
    for evaluation in entite.evaluations:
        Score.query.filter_by(evaluation_id=evaluation.id).delete()
        db.session.delete(evaluation)
    db.session.delete(entite)
    db.session.commit()
    flash(f"Entité « {nom} » supprimée.", "success")
    return redirect(url_for("entites_list"))


# ──────────────────────────────────────────────
# Routes — Sites
# ──────────────────────────────────────────────

@app.route("/sites")
def sites_list():
    sites = Site.query.order_by(Site.nom).all()
    return render_template("sites.html", sites=sites)


@app.route("/sites/new", methods=["GET", "POST"])
def site_new():
    entites = Entite.query.order_by(Entite.nom).all()
    if request.method == "POST":
        site = Site(
            nom=request.form["nom"],
            url=request.form.get("url", ""),
            description=request.form.get("description", ""),
            organisation_id=int(request.form["organisation_id"]),
        )
        db.session.add(site)
        db.session.commit()
        flash(f"Site « {site.nom} » créé.", "success")
        return redirect(url_for("sites_list"))
    return render_template("site_form.html", site=None, entites=entites)


@app.route("/sites/<int:site_id>/delete", methods=["POST"])
def site_delete(site_id):
    site = Site.query.get_or_404(site_id)
    nom = site.nom
    for evaluation in site.evaluations:
        Score.query.filter_by(evaluation_id=evaluation.id).delete()
        db.session.delete(evaluation)
    db.session.delete(site)
    db.session.commit()
    flash(f"Site « {nom} » supprimé.", "success")
    return redirect(url_for("sites_list"))


# ──────────────────────────────────────────────
# Routes — Campagnes
# ──────────────────────────────────────────────

@app.route("/campagnes/new", methods=["GET", "POST"])
def campagne_new():
    if request.method == "POST":
        campagne = Campagne(
            label=request.form["label"],
            date_debut=date.fromisoformat(request.form["date_debut"]),
            date_fin=date.fromisoformat(request.form["date_fin"]) if request.form.get("date_fin") else None,
        )
        db.session.add(campagne)
        db.session.commit()
        flash(f"Campagne « {campagne.label} » créée.", "success")
        return redirect(url_for("campagnes_list"))
    return render_template("campagne_form.html")


@app.route("/campagnes")
def campagnes_list():
    campagnes = Campagne.query.order_by(Campagne.date_debut.desc()).all()
    return render_template("campagnes.html", campagnes=campagnes)


@app.route("/campagnes/<int:campagne_id>/delete", methods=["POST"])
def campagne_delete(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    label = campagne.label
    db.session.delete(campagne)
    db.session.commit()
    flash(f"Campagne « {label} » supprimée.", "success")
    return redirect(url_for("campagnes_list"))


# ──────────────────────────────────────────────
# Routes — Évaluation
# ──────────────────────────────────────────────

@app.route("/evaluation/new", methods=["GET", "POST"])
def evaluation_new():
    """Crée une nouvelle évaluation (choix référentiel + cible)."""
    referentiels = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    campagnes = Campagne.query.filter_by(statut="en_cours").order_by(Campagne.date_debut.desc()).all()
    entites = Entite.query.order_by(Entite.nom).all()
    sites = Site.query.order_by(Site.nom).all()

    if request.method == "POST":
        referentiel_id = int(request.form["referentiel_id"])
        ref = ReferentielVersion.query.get_or_404(referentiel_id)

        eval_kwargs = {
            "referentiel_id": ref.id,
            "evaluateur": request.form.get("evaluateur", ""),
        }

        if ref.cible == "organisation":
            eval_kwargs["entite_id"] = int(request.form["entite_id"])
            campagne_id = request.form.get("campagne_id")
            if campagne_id:
                eval_kwargs["campagne_id"] = int(campagne_id)
        else:
            eval_kwargs["site_id"] = int(request.form["site_id"])

        evaluation = Evaluation(**eval_kwargs)

        try:
            db.session.add(evaluation)
            db.session.commit()
            return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))
        except IntegrityError:
            db.session.rollback()
            flash(
                "Une évaluation similaire existe déjà. "
                "Consultez la liste des évaluations pour la retrouver ou la supprimer.",
                "warning",
            )
            return redirect(url_for("evaluations_list"))

    return render_template("evaluation_new.html",
        referentiels=referentiels, campagnes=campagnes,
        entites=entites, sites=sites,
    )


@app.route("/evaluations")
def evaluations_list():
    evaluations = Evaluation.query.order_by(Evaluation.date_evaluation.desc()).all()
    return render_template("evaluations.html", evaluations=evaluations)


@app.route("/evaluations/<int:evaluation_id>/delete", methods=["POST"])
def evaluation_delete(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    cible_nom = evaluation.cible_nom
    ctx = evaluation.campagne.label if evaluation.campagne_id else "déclaration"
    db.session.delete(evaluation)
    db.session.commit()
    flash(f"Évaluation de « {cible_nom} » ({ctx}) supprimée.", "success")
    return redirect(url_for("evaluations_list"))


@app.route("/evaluation/<int:evaluation_id>/fill", methods=["GET", "POST"])
def evaluation_fill(evaluation_id):
    """Formulaire de saisie des scores — toutes les capacités."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    ref = evaluation.referentiel
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    # Scores existants (pour pré-remplir)
    existing_scores = {s.capacite_id: s for s in evaluation.scores}

    if request.method == "POST":
        # Sauvegarder les scores
        for dim in dimensions:
            for cap in dim.capacites:
                field_name = f"cap_{cap.id}"
                niveau_val = request.form.get(field_name)
                if niveau_val:
                    niveau_val = int(niveau_val)
                    justification = request.form.get(f"just_{cap.id}", "")

                    if cap.id in existing_scores:
                        existing_scores[cap.id].niveau = niveau_val
                        existing_scores[cap.id].justification = justification
                    else:
                        score = Score(
                            evaluation_id=evaluation.id,
                            capacite_id=cap.id,
                            niveau=niveau_val,
                            justification=justification,
                        )
                        db.session.add(score)

        # Statut
        action = request.form.get("action", "save")
        if action == "validate":
            evaluation.statut = "validee"
            evaluation.date_evaluation = datetime.utcnow()
            flash("Évaluation validée.", "success")
        else:
            flash("Brouillon sauvegardé.", "info")

        db.session.commit()
        if action == "validate":
            return redirect(url_for("evaluation_results", evaluation_id=evaluation.id))
        return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))

    nb_capacites = sum(len(dim.capacites) for dim in dimensions)

    return render_template(
        "evaluation_fill.html",
        evaluation=evaluation,
        dimensions=dimensions,
        existing_scores=existing_scores,
        nb_capacites=nb_capacites,
    )


@app.route("/evaluation/<int:evaluation_id>/results")
def evaluation_results(evaluation_id):
    """Résultats d'une évaluation."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    ref = evaluation.referentiel
    dim_scores = compute_scores_by_dimension(evaluation)
    max_niveau = get_max_niveau(ref)

    # Détail par capacité
    detail = []
    for score in evaluation.scores:
        cap = score.capacite
        detail.append({
            "dimension": cap.dimension.nom,
            "dim_numero": cap.dimension.numero,
            "capacite": cap.nom,
            "cap_numero": cap.numero,
            "portee": cap.portee,
            "niveau": score.niveau,
            "justification": score.justification or "",
        })
    detail.sort(key=lambda x: (x["dim_numero"], x["cap_numero"]))

    # Données DSFR Chart : radar
    dim_labels = [f"{d['numero']}. {d['nom']}" for d in dim_scores.values()]
    dim_moyennes = [d["moyenne"] for d in dim_scores.values()]
    radar_x = json.dumps([dim_labels])
    radar_y = json.dumps([dim_moyennes])

    return render_template(
        "evaluation_results.html",
        evaluation=evaluation,
        dim_scores=dim_scores,
        detail=detail,
        radar_x=radar_x,
        radar_y=radar_y,
        max_niveau=max_niveau,
    )


# ──────────────────────────────────────────────
# Routes — Dashboard campagne (vue globale)
# ──────────────────────────────────────────────

@app.route("/campagne/<int:campagne_id>/dashboard")
def campagne_dashboard(campagne_id):
    """Dashboard global d'une campagne — moyennes, écarts, comparaison."""
    campagne = Campagne.query.get_or_404(campagne_id)
    evaluations = Evaluation.query.filter_by(campagne_id=campagne.id).all()

    stats = compute_global_stats(campagne)

    # Déterminer le référentiel depuis les évaluations
    validated = [ev for ev in evaluations if ev.statut == "validee"]
    ref = validated[0].referentiel if validated else (get_active_referentiel() or ReferentielVersion.query.first())
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    # Données par cible (entité ou site) pour le radar
    entites_data = []
    for ev in validated:
        dim_scores = compute_scores_by_dimension(ev)
        entites_data.append({
            "nom": ev.cible_nom,
            "scores": {d["numero"]: d["moyenne"] for d in dim_scores.values()},
        })

    # Heatmap data: cible × capacité
    heatmap = []
    for ev in validated:
        row = {"entite": ev.cible_nom, "scores": {}}
        for s in ev.scores:
            row["scores"][s.capacite.numero] = s.niveau
        heatmap.append(row)

    # Liste des capacités pour les en-têtes de la heatmap
    all_capacites = []
    for dim in dimensions:
        for cap in dim.capacites:
            all_capacites.append({"numero": cap.numero, "nom": cap.nom, "dim_nom": dim.nom})

    # Données DSFR Chart
    chart_radar_x = []
    chart_radar_y = []
    chart_radar_names = []
    chart_bar_x = []
    chart_bar_y_moy = []
    chart_bar_y_ecart = []

    if stats:
        dim_labels = [f"{s['numero']}. {s['nom']}" for s in stats.values()]
        dim_nums = [s["numero"] for s in stats.values()]

        # Radar comparatif : une série par cible + moyenne
        for ent in entites_data:
            chart_radar_x.append(dim_labels)
            chart_radar_y.append([ent["scores"].get(n, 0) for n in dim_nums])
            chart_radar_names.append(ent["nom"])
        # Ajouter la moyenne
        chart_radar_x.append(dim_labels)
        chart_radar_y.append([s["moyenne"] for s in stats.values()])
        chart_radar_names.append("Moyenne")

        # Bar chart écarts : 2 séries
        chart_bar_x = [dim_labels, dim_labels]
        chart_bar_y_moy = [s["moyenne"] for s in stats.values()]
        chart_bar_y_ecart = [s["ecart_type"] for s in stats.values()]

    return render_template(
        "campagne_dashboard.html",
        campagne=campagne,
        evaluations=evaluations,
        stats=stats,
        dimensions=dimensions,
        referentiel=ref,
        entites_data=json.dumps(entites_data),
        heatmap=heatmap,
        all_capacites=all_capacites,
        chart_radar_x=json.dumps(chart_radar_x),
        chart_radar_y=json.dumps(chart_radar_y),
        chart_radar_names=json.dumps(chart_radar_names),
        chart_bar_x=json.dumps(chart_bar_x),
        chart_bar_y=json.dumps([chart_bar_y_moy, chart_bar_y_ecart]),
        chart_bar_names=json.dumps(["Moyenne", "Écart-type"]),
    )


# ──────────────────────────────────────────────
# Routes — Évolution dans le temps
# ──────────────────────────────────────────────

@app.route("/entite/<int:entite_id>/evolution")
def entite_evolution(entite_id):
    """Évolution d'une entité à travers les campagnes."""
    entite = Entite.query.get_or_404(entite_id)
    evaluations = Evaluation.query.filter_by(
        entite_id=entite.id, statut="validee"
    ).order_by(Evaluation.date_evaluation).all()

    timeline = []
    for ev in evaluations:
        dim_scores = compute_scores_by_dimension(ev)
        label = ev.campagne.label if ev.campagne_id else ev.date_evaluation.strftime("%Y-%m-%d")
        timeline.append({
            "campagne": label,
            "date": ev.date_evaluation.strftime("%Y-%m-%d"),
            "referentiel": ev.referentiel.label,
            "scores": {d["numero"]: d["moyenne"] for d in dim_scores.values()},
        })

    # Utiliser le référentiel de la dernière évaluation, sinon le référentiel actif
    if evaluations:
        ref = evaluations[-1].referentiel
    else:
        ref = get_active_referentiel() or ReferentielVersion.query.first()
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    # Données DSFR Chart
    dim_labels = [f"{d.numero}. {d.nom}" for d in dimensions]
    dim_nums = [d.numero for d in dimensions]

    # Line chart : une série par dimension
    campagne_labels = [t["campagne"] for t in timeline]
    line_x = []
    line_y = []
    line_names = []
    for dim in dimensions:
        line_x.append(campagne_labels)
        line_y.append([t["scores"].get(dim.numero, 0) for t in timeline])
        line_names.append(f"{dim.numero}. {dim.nom}")

    # Radar dernière évaluation
    last_radar_x = []
    last_radar_y = []
    if timeline:
        last = timeline[-1]
        last_radar_x = [dim_labels]
        last_radar_y = [[last["scores"].get(n, 0) for n in dim_nums]]

    return render_template(
        "entite_evolution.html",
        entite=entite,
        timeline=json.dumps(timeline),
        dimensions=dimensions,
        line_x=json.dumps(line_x),
        line_y=json.dumps(line_y),
        line_names=json.dumps(line_names),
        last_radar_x=json.dumps(last_radar_x),
        last_radar_y=json.dumps(last_radar_y),
    )


# ──────────────────────────────────────────────
# API JSON (pour les graphiques dynamiques)
# ──────────────────────────────────────────────

@app.route("/api/evaluation/<int:evaluation_id>/scores")
def api_evaluation_scores(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    dim_scores = compute_scores_by_dimension(evaluation)
    return jsonify({
        "cible": evaluation.cible_nom,
        "referentiel": evaluation.referentiel.label,
        "dimensions": [
            {"nom": d["nom"], "numero": d["numero"], "moyenne": d["moyenne"]}
            for d in dim_scores.values()
        ],
    })


# ──────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
