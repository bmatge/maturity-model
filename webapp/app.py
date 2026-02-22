"""
Webapp de suivi de maturité de la communication numérique ministérielle.
Flask + SQLite + Bootstrap 5 + Chart.js
"""

import os
import json
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, ReferentielVersion, Dimension, Capacite, NiveauCritere
from models import Entite, Campagne, Evaluation, Score
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "maturity.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ──────────────────────────────────────────────
# Initialisation
# ──────────────────────────────────────────────

@app.before_request
def ensure_db():
    """Crée les tables et seed au premier appel."""
    if not getattr(app, "_db_ready", False):
        db.create_all()
        from seed import seed_referentiel, seed_demo_entites
        seed_referentiel()
        seed_demo_entites()
        app._db_ready = True


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def get_active_referentiel():
    return ReferentielVersion.query.filter_by(is_active=True).first()


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

    ref = campagne.referentiel
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
    return render_template("index.html", campagnes=campagnes, entites=entites)


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


# ──────────────────────────────────────────────
# Routes — Campagnes
# ──────────────────────────────────────────────

@app.route("/campagnes/new", methods=["GET", "POST"])
def campagne_new():
    ref = get_active_referentiel()
    if request.method == "POST":
        campagne = Campagne(
            label=request.form["label"],
            referentiel_id=ref.id,
            date_debut=date.fromisoformat(request.form["date_debut"]),
            date_fin=date.fromisoformat(request.form["date_fin"]) if request.form.get("date_fin") else None,
        )
        db.session.add(campagne)
        db.session.commit()
        flash(f"Campagne « {campagne.label} » créée.", "success")
        return redirect(url_for("index"))
    return render_template("campagne_form.html", referentiel=ref)


# ──────────────────────────────────────────────
# Routes — Évaluation
# ──────────────────────────────────────────────

@app.route("/evaluation/new", methods=["GET", "POST"])
def evaluation_new():
    """Crée une nouvelle évaluation (choix entité + campagne)."""
    campagnes = Campagne.query.filter_by(statut="en_cours").order_by(Campagne.date_debut.desc()).all()
    entites = Entite.query.order_by(Entite.nom).all()

    if request.method == "POST":
        evaluation = Evaluation(
            campagne_id=int(request.form["campagne_id"]),
            entite_id=int(request.form["entite_id"]),
            evaluateur=request.form.get("evaluateur", ""),
        )
        db.session.add(evaluation)
        db.session.commit()
        return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))

    return render_template("evaluation_new.html", campagnes=campagnes, entites=entites)


@app.route("/evaluation/<int:evaluation_id>/fill", methods=["GET", "POST"])
def evaluation_fill(evaluation_id):
    """Formulaire de saisie des scores — toutes les capacités."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    ref = evaluation.campagne.referentiel
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

    return render_template(
        "evaluation_fill.html",
        evaluation=evaluation,
        dimensions=dimensions,
        existing_scores=existing_scores,
    )


@app.route("/evaluation/<int:evaluation_id>/results")
def evaluation_results(evaluation_id):
    """Résultats d'une évaluation."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    dim_scores = compute_scores_by_dimension(evaluation)

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

    return render_template(
        "evaluation_results.html",
        evaluation=evaluation,
        dim_scores=dim_scores,
        detail=detail,
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
    ref = campagne.referentiel
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    # Données par entité pour le radar
    entites_data = []
    for ev in evaluations:
        if ev.statut != "validee":
            continue
        dim_scores = compute_scores_by_dimension(ev)
        entites_data.append({
            "nom": ev.entite.nom,
            "scores": {d["numero"]: d["moyenne"] for d in dim_scores.values()},
        })

    # Heatmap data: entité × capacité
    heatmap = []
    for ev in evaluations:
        if ev.statut != "validee":
            continue
        row = {"entite": ev.entite.nom, "scores": {}}
        for s in ev.scores:
            row["scores"][s.capacite.numero] = s.niveau
        heatmap.append(row)

    # Liste des capacités pour les en-têtes de la heatmap
    all_capacites = []
    for dim in dimensions:
        for cap in dim.capacites:
            all_capacites.append({"numero": cap.numero, "nom": cap.nom, "dim_nom": dim.nom})

    return render_template(
        "campagne_dashboard.html",
        campagne=campagne,
        evaluations=evaluations,
        stats=stats,
        dimensions=dimensions,
        entites_data=json.dumps(entites_data),
        heatmap=heatmap,
        all_capacites=all_capacites,
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
        timeline.append({
            "campagne": ev.campagne.label,
            "date": ev.date_evaluation.strftime("%Y-%m-%d"),
            "scores": {d["numero"]: d["moyenne"] for d in dim_scores.values()},
        })

    ref = get_active_referentiel()
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    return render_template(
        "entite_evolution.html",
        entite=entite,
        timeline=json.dumps(timeline),
        dimensions=dimensions,
    )


# ──────────────────────────────────────────────
# API JSON (pour les graphiques dynamiques)
# ──────────────────────────────────────────────

@app.route("/api/evaluation/<int:evaluation_id>/scores")
def api_evaluation_scores(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    dim_scores = compute_scores_by_dimension(evaluation)
    return jsonify({
        "entite": evaluation.entite.nom,
        "campagne": evaluation.campagne.label,
        "dimensions": [
            {"nom": d["nom"], "numero": d["numero"], "moyenne": d["moyenne"]}
            for d in dim_scores.values()
        ],
    })


# ──────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
