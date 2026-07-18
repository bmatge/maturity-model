"""
Webapp de suivi de maturité numérique — multi-référentiel (organisations + sites).
Flask + SQLite + DSFR natif + dsfr-data (charts).

UI issue de la maquette Claude Design « Maturité numérique.dc.html » :
3 espaces par rôle — Répondant (Camille), Pilote (Nadia), Lecteur public (Marc).
Comptes utilisateurs minimaux en attendant Authentik (cf. tasks/todo.md).
"""

import csv
import io
import json
import os
from datetime import date, datetime
from functools import wraps

from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from models import db, ReferentielVersion, Dimension, Capacite, NiveauCritere
from models import Entite, Site, Campagne, CampagneParticipant, Evaluation, Score, User
import mailer
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "maturity-poc-dev-key")
db_path = os.environ.get("DATABASE_PATH", os.path.join(os.path.abspath(os.path.dirname(__file__)), "maturity.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ──────────────────────────────────────────────
# Initialisation / migrations
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

    # Migration 3 : recréer evaluation avec le bon schéma (campagne_id nullable, site_id)
    eval_info = list(conn.execute(text("PRAGMA table_info(evaluation)")))
    eval_col_names = [row[1] for row in eval_info]
    campagne_col = [row for row in eval_info if row[1] == "campagne_id"]
    needs_rebuild = (campagne_col and campagne_col[0][3] == 1) or ("site_id" not in eval_col_names)
    if needs_rebuild:
        conn.execute(text("DROP TABLE IF EXISTS evaluation_new"))
        conn.execute(text(
            "CREATE TABLE evaluation_new ("
            "id INTEGER PRIMARY KEY, referentiel_id INTEGER NOT NULL REFERENCES referentiel_version(id), "
            "campagne_id INTEGER REFERENCES campagne(id), "
            "entite_id INTEGER REFERENCES entite(id), site_id INTEGER REFERENCES site(id), "
            "evaluateur VARCHAR(200), date_evaluation DATETIME, statut VARCHAR(20) DEFAULT 'brouillon', "
            "commentaire_global TEXT)"
        ))
        src_cols = "id, referentiel_id, campagne_id, entite_id, evaluateur, date_evaluation, statut, commentaire_global"
        dst_cols = src_cols
        if "site_id" in eval_col_names:
            src_cols += ", site_id"
            dst_cols += ", site_id"
        conn.execute(text(
            f"INSERT INTO evaluation_new ({dst_cols}) SELECT {src_cols} FROM evaluation"
        ))
        conn.execute(text("DROP TABLE evaluation"))
        conn.execute(text("ALTER TABLE evaluation_new RENAME TO evaluation"))
        conn.commit()

    # Migration 5 : email de contact des entités (relances/invitations par mail)
    ent_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(entite)"))]
    if "email_contact" not in ent_cols:
        conn.execute(text("ALTER TABLE entite ADD COLUMN email_contact VARCHAR(200)"))
        conn.commit()

    # Migration 4 : referentiel_id (nullable) sur campagne — comparabilité + invitations
    camp_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(campagne)"))]
    if "referentiel_id" not in camp_cols:
        conn.execute(text(
            "ALTER TABLE campagne ADD COLUMN referentiel_id INTEGER REFERENCES referentiel_version(id)"
        ))
        # Déduire des évaluations existantes (référentiel majoritaire)
        conn.execute(text(
            "UPDATE campagne SET referentiel_id = ("
            "  SELECT referentiel_id FROM evaluation"
            "  WHERE evaluation.campagne_id = campagne.id"
            "  GROUP BY referentiel_id ORDER BY COUNT(*) DESC LIMIT 1"
            ") WHERE referentiel_id IS NULL"
        ))
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
        if not SSO_MODE:
            seed_demo_users()
        app._db_ready = True


def seed_demo_users():
    """Comptes de démonstration (dev uniquement — en SSO les comptes naissent au 1er login)."""
    if User.query.first():
        return
    sante = Entite.query.filter_by(nom="Bureau com — Santé").first()
    users = [
        User(nom="Nadia Bensaïd", email="nadia.bensaid@finances.gouv.fr",
             role="pilote", scope_type="global"),
        User(nom="Camille Durand", email="camille.durand@finances.gouv.fr",
             role="repondant", scope_type="entite" if sante else "global",
             scope_entite_id=sante.id if sante else None),
        User(nom="Admin technique", email="admin@finances.gouv.fr",
             role="admin", scope_type="global"),
    ]
    db.session.add_all(users)
    db.session.commit()


# ──────────────────────────────────────────────
# Identité & rôles
#
# Deux modes :
# - SSO (SSO_HEADERS=1, déploiement lab derrière le proxy Authentik) :
#   l'identité vient des en-têtes X-authentik-* posés par Traefik
#   (authResponseHeaders — non spoofables derrière le middleware). Le rôle
#   applicatif est dérivé des groupes Authentik maturity-admin / maturity-pilote /
#   maturity-repondant ; un membre du lab sans groupe maturity-* est lecteur.
# - Dev (défaut) : sélecteur d'identité en session (pré-Authentik).
# ──────────────────────────────────────────────

SSO_MODE = os.environ.get("SSO_HEADERS") == "1"
SSO_ROLE_GROUPS = [("maturity-admin", "admin"),
                   ("maturity-pilote", "pilote"),
                   ("maturity-repondant", "repondant")]


def sso_identity():
    """(email, nom, rôle) depuis les en-têtes Authentik, ou None hors SSO."""
    email = (request.headers.get("X-Authentik-Email") or "").strip().lower()
    if not (SSO_MODE and email):
        return None
    nom = request.headers.get("X-Authentik-Name") or request.headers.get("X-Authentik-Username") or email
    groups = {g.strip().lower() for g in (request.headers.get("X-Authentik-Groups") or "").split("|") if g.strip()}
    role = next((r for g, r in SSO_ROLE_GROUPS if g in groups), None)
    return email, nom, role


def current_user():
    ident = sso_identity()
    if ident:
        email, nom, role = ident
        if role is None:
            return None  # membre du lab sans groupe maturity-* → lecteur
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(nom=nom, email=email, role=role, scope_type="global")
            db.session.add(user)
            db.session.commit()
        elif user.nom != nom or user.role != role:
            # les groupes Authentik sont la source de vérité du rôle
            user.nom, user.role = nom, role
            db.session.commit()
        return user
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None


def current_role():
    """Rôle courant : celui du compte, ou « lecteur » (public) sans compte."""
    user = current_user()
    return user.role if user else "lecteur"


# Rôles cumulatifs : admin ⊃ pilote ⊃ répondant ⊃ lecteur.
ROLE_HIERARCHY = {
    "admin": ("admin", "pilote", "repondant", "lecteur"),
    "pilote": ("pilote", "repondant", "lecteur"),
    "repondant": ("repondant", "lecteur"),
    "lecteur": ("lecteur",),
}

# Espaces de navigation, du plus outillé au plus consultatif.
SPACES = [
    ("pilote", "Pilotage", ("pilote", "admin")),
    ("repondant", "Mon espace", ("repondant", "pilote", "admin")),
    ("lecteur", "Restitution", ("lecteur", "repondant", "pilote", "admin")),
]


def effective_roles():
    return ROLE_HIERARCHY.get(current_role(), ("lecteur",))


def accessible_spaces():
    role = current_role()
    return [(key, label) for key, label, roles in SPACES if role in roles]


def current_space():
    """Espace de navigation courant (choisi en session, borné aux espaces accessibles)."""
    spaces = [k for k, _ in accessible_spaces()]
    chosen = session.get("space")
    return chosen if chosen in spaces else spaces[0]


def require_roles(*roles):
    """Guard cumulatif : un rôle supérieur accède aux pages des rôles inférieurs."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not set(effective_roles()) & set(roles):
                flash("Cette page est réservée au rôle "
                      + " / ".join(roles) + ".", "warning")
                return redirect(url_for("home"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/espace/<space>")
def switch_space(space):
    """Bascule d'espace de navigation (rôles cumulatifs)."""
    if space in [k for k, _ in accessible_spaces()]:
        session["space"] = space
    return redirect({"repondant": url_for("mes_evaluations"),
                     "lecteur": url_for("restitution")}.get(space, url_for("home")))


@app.route("/login-as", methods=["POST"])
def login_as():
    """Sélecteur d'identité (dev uniquement — en SSO l'identité vient d'Authentik)."""
    if SSO_MODE:
        flash("L'identité est gérée par le SSO Authentik.", "info")
        return redirect(url_for("home"))
    uid = request.form.get("user_id", "")
    if uid == "public" or not uid:
        session.pop("user_id", None)
    else:
        user = db.session.get(User, int(uid))
        if user:
            session["user_id"] = user.id
    return redirect(request.form.get("next") or url_for("home"))


# ──────────────────────────────────────────────
# Helpers de calcul (niveau 0 = non applicable, exclu)
# ──────────────────────────────────────────────

def scored(scores):
    """Filtre les scores exploitables (exclut les non-applicables)."""
    return [s for s in scores if s.niveau > 0]


def compute_scores_by_dimension(evaluation):
    """Retourne {dimension_id: {nom, numero, moyenne, nb_capacites, scores}} (NA exclus)."""
    result = {}
    for score in scored(evaluation.scores):
        cap = score.capacite
        dim = cap.dimension
        if dim.id not in result:
            result[dim.id] = {"nom": dim.nom, "numero": dim.numero, "scores": []}
        result[dim.id]["scores"].append(score.niveau)

    for data in result.values():
        data["moyenne"] = round(sum(data["scores"]) / len(data["scores"]), 2)
        data["nb_capacites"] = len(data["scores"])

    return dict(sorted(result.items(), key=lambda x: x[1]["numero"]))


def global_score(evaluation):
    """Score global unifié : moyenne des moyennes de dimension (NA exclus)."""
    dim_scores = compute_scores_by_dimension(evaluation)
    moyennes = [d["moyenne"] for d in dim_scores.values()]
    return round(sum(moyennes) / len(moyennes), 2) if moyennes else 0


def get_max_niveau(ref):
    """Nombre max de niveaux pour un référentiel (3 ou 4)."""
    for dim in ref.dimensions:
        if dim.capacites and dim.capacites[0].niveaux:
            return max(n.niveau for n in dim.capacites[0].niveaux)
    return 4


def ref_counts(ref):
    """(nb dimensions, nb capacités) d'un référentiel."""
    nb_caps = sum(len(d.capacites) for d in ref.dimensions)
    return len(ref.dimensions), nb_caps


def eval_progress(evaluation):
    """(nb renseignées [NA inclus], nb total de capacités du référentiel)."""
    total = sum(len(d.capacites) for d in evaluation.referentiel.dimensions)
    return len(evaluation.scores), total


def score_color(pct):
    """Convention maquette : <50 % alerte, 50-75 % en progrès, >75 % solide."""
    if pct < 50:
        return "error"
    if pct < 75:
        return "warning"
    return "success"


def eval_summary(evaluation):
    """Résumé d'une évaluation pour les listes/cartes."""
    done, total = eval_progress(evaluation)
    max_niv = get_max_niveau(evaluation.referentiel)
    score = global_score(evaluation)
    pct = round(score / max_niv * 100) if max_niv else 0
    return {
        "eval": evaluation,
        "done": done, "total": total,
        "pct_progress": round(done / total * 100) if total else 0,
        "score": score, "max": max_niv, "pct": pct,
        "color": score_color(pct),
    }


def campagne_stats(campagne):
    """Participation d'une campagne : participants attendus × évaluations."""
    participants = CampagneParticipant.query.filter_by(campagne_id=campagne.id).all()
    evals = Evaluation.query.filter_by(campagne_id=campagne.id).all()
    evals_by_entite = {}
    for ev in evals:
        if ev.entite_id:
            evals_by_entite.setdefault(ev.entite_id, []).append(ev)

    rows = []
    if participants:
        for p in participants:
            p_evals = evals_by_entite.get(p.entite_id, [])
            validee = next((e for e in p_evals if e.statut == "validee"), None)
            brouillon = next((e for e in p_evals if e.statut == "brouillon"), None)
            if validee:
                statut, ev = "validee", validee
            elif brouillon:
                statut, ev = "brouillon", brouillon
            else:
                statut, ev = "nonstart", None
            row = {"participant": p, "entite": p.entite, "statut": statut, "eval": ev}
            if ev:
                row["done"], row["total"] = eval_progress(ev)
                row["evaluateur"] = ev.evaluateur
            else:
                row["evaluateur"] = p.evaluateur
            rows.append(row)
        attendus = len(participants)
    else:
        # Pas de périmètre défini : on retombe sur les évaluations existantes
        for ev in evals:
            row = {"participant": None,
                   "entite": ev.entite if ev.entite_id else None,
                   "site": ev.site if ev.site_id else None,
                   "statut": ev.statut if ev.statut == "validee" else "brouillon",
                   "eval": ev, "evaluateur": ev.evaluateur}
            row["done"], row["total"] = eval_progress(ev)
            rows.append(row)
        attendus = len(evals)

    valides = sum(1 for r in rows if r["statut"] == "validee")
    brouillons = sum(1 for r in rows if r["statut"] == "brouillon")
    manquants = sum(1 for r in rows if r["statut"] == "nonstart")
    return {
        "rows": rows, "attendus": attendus, "valides": valides,
        "brouillons": brouillons, "manquants": manquants,
        "pct": round(valides / attendus * 100) if attendus else 0,
        "has_perimetre": bool(participants),
    }


def compute_global_stats(campagne):
    """Stats par dimension (moyenne, écart-type, min, max) sur les éval. validées."""
    evaluations = Evaluation.query.filter_by(campagne_id=campagne.id, statut="validee").all()
    if not evaluations:
        return None

    ref = campagne.referentiel or evaluations[0].referentiel
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    stats = {}
    for dim in dimensions:
        dim_scores = []
        for ev in evaluations:
            scores = [s.niveau for s in scored(ev.scores) if s.capacite.dimension_id == dim.id]
            if scores:
                dim_scores.append(sum(scores) / len(scores))
        if dim_scores:
            mean = sum(dim_scores) / len(dim_scores)
            variance = sum((x - mean) ** 2 for x in dim_scores) / len(dim_scores)
            stats[dim.id] = {
                "nom": dim.nom, "numero": dim.numero,
                "moyenne": round(mean, 2),
                "ecart_type": round(variance ** 0.5, 2),
                "min": round(min(dim_scores), 2),
                "max": round(max(dim_scores), 2),
                "nb_entites": len(dim_scores),
            }
    return stats


def last_validated_by_ref(entite_id=None, site_id=None):
    """{referentiel_id: dernière évaluation validée} pour une cible."""
    q = Evaluation.query.filter_by(statut="validee")
    if entite_id:
        q = q.filter_by(entite_id=entite_id)
    else:
        q = q.filter_by(site_id=site_id)
    result = {}
    for ev in q.order_by(Evaluation.date_evaluation.desc()).all():
        if ev.referentiel_id not in result:
            result[ev.referentiel_id] = ev
    return result


def target_scores_summary(entite_id=None, site_id=None):
    """[{ref, score, max, pct, color, eval}] par référentiel (dernière validée)."""
    out = []
    for ev in last_validated_by_ref(entite_id=entite_id, site_id=site_id).values():
        max_niv = get_max_niveau(ev.referentiel)
        score = global_score(ev)
        pct = round(score / max_niv * 100) if max_niv else 0
        out.append({"ref": ev.referentiel, "score": score, "max": max_niv,
                    "pct": pct, "color": score_color(pct), "eval": ev})
    out.sort(key=lambda x: x["ref"].label)
    return out


def scoped_evaluations_query():
    """Évaluations visibles par l'utilisateur courant (droit global/entité/site)."""
    q = Evaluation.query
    user = current_user()
    if user and user.scope_type == "entite" and user.scope_entite_id:
        site_ids = [s.id for s in Site.query.filter_by(organisation_id=user.scope_entite_id)]
        q = q.filter((Evaluation.entite_id == user.scope_entite_id)
                     | (Evaluation.site_id.in_(site_ids) if site_ids else False))
    elif user and user.scope_type == "site" and user.scope_site_id:
        q = q.filter(Evaluation.site_id == user.scope_site_id)
    return q


# ──────────────────────────────────────────────
# Contexte global (header, sidemenu)
# ──────────────────────────────────────────────

NAVS = {
    "repondant": [
        {"endpoint": "mes_evaluations", "label": "Mes évaluations", "icon": "fr-icon-home-4-line"},
        {"endpoint": "evaluation_new", "label": "Démarrer", "icon": "fr-icon-add-circle-line"},
        {"endpoint": "referentiel_view", "label": "Le référentiel", "icon": "fr-icon-book-2-line"},
    ],
    "pilote": [
        {"endpoint": "home", "label": "Tableau de bord", "icon": "fr-icon-dashboard-3-line"},
        {"endpoint": "campagnes_list", "label": "Campagnes", "icon": "fr-icon-calendar-2-line"},
        {"endpoint": "evaluations_list", "label": "Évaluations", "icon": "fr-icon-survey-line"},
        {"endpoint": "entites_list", "label": "Organisations", "icon": "fr-icon-building-line"},
        {"endpoint": "sites_list", "label": "Sites web", "icon": "fr-icon-earth-line"},
        {"endpoint": "referentiels_admin", "label": "Référentiels", "icon": "fr-icon-stack-line"},
        {"endpoint": "users_list", "label": "Utilisateurs & rôles", "icon": "fr-icon-team-line"},
        {"endpoint": "referentiel_view", "label": "Le référentiel", "icon": "fr-icon-book-2-line"},
    ],
    "lecteur": [
        {"endpoint": "restitution", "label": "Vue d'ensemble", "icon": "fr-icon-slideshow-line"},
        {"endpoint": "restitution_orgs", "label": "Fiche organisation", "icon": "fr-icon-building-line"},
        {"endpoint": "evolution_view", "label": "Évolution dans le temps", "icon": "fr-icon-line-chart-line"},
        {"endpoint": "comparer", "label": "Comparer", "icon": "fr-icon-scales-3-line"},
        {"endpoint": "plan_action", "label": "Plan d'action", "icon": "fr-icon-flag-line"},
        {"endpoint": "exporter", "label": "Exporter / partager", "icon": "fr-icon-download-line"},
        {"endpoint": "referentiel_view", "label": "Le référentiel", "icon": "fr-icon-book-2-line"},
    ],
}
NAVS["admin"] = NAVS["pilote"]

SIDE_CARDS = {
    "repondant": ("Besoin d'aide ?",
                  "Chaque niveau décrit une situation concrète : choisissez celle qui vous ressemble le plus."),
    "lecteur": ("Lecture rapide",
                "Repères : moins de 50 % = alerte, 50–75 % = en progrès, plus de 75 % = solide."),
}


@app.context_processor
def inject_layout():
    role = current_role()
    user = current_user()
    space = current_space()
    nav = list(NAVS.get(space, NAVS["lecteur"]))

    extra_nav = []
    if space == "repondant":
        draft = scoped_evaluations_query().filter_by(statut="brouillon") \
            .order_by(Evaluation.date_evaluation.desc()).first()
        if draft:
            done, total = eval_progress(draft)
            extra_nav.append({"url": url_for("evaluation_fill", evaluation_id=draft.id),
                              "label": "Évaluation en cours", "icon": "fr-icon-edit-line",
                              "badge": f"{done}/{total}", "endpoint": "evaluation_fill"})
        last_valid = scoped_evaluations_query().filter_by(statut="validee") \
            .order_by(Evaluation.date_evaluation.desc()).first()
        if last_valid:
            extra_nav.append({"url": url_for("evaluation_results", evaluation_id=last_valid.id),
                              "label": "Mes résultats", "icon": "fr-icon-pie-chart-2-line",
                              "endpoint": "evaluation_results"})
        nav = nav[:1] + extra_nav[:1] + nav[1:2] + extra_nav[1:] + nav[2:]

    # Carte contextuelle sidebar
    if space == "pilote":
        camp = Campagne.query.filter_by(statut="en_cours").order_by(Campagne.date_debut.desc()).first()
        if camp:
            st = campagne_stats(camp)
            side_card = (camp.label,
                         f"{st['attendus']} entités attendues · {st['valides']} validées · "
                         f"{st['brouillons']} en brouillon · {st['manquants']} non commencées.")
        else:
            side_card = ("Aucune campagne en cours",
                         "Créez une campagne pour lancer une vague d'évaluations.")
    else:
        side_card = SIDE_CARDS.get(space, SIDE_CARDS["lecteur"])

    nb_campagnes_en_cours = Campagne.query.filter_by(statut="en_cours").count()
    return {
        "sso_mode": SSO_MODE,
        "mail_enabled": mailer.enabled(),
        "current_user_obj": user,
        "current_role": role,
        "role_label": {"repondant": "Répondant", "pilote": "Pilote",
                       "admin": "Administrateur", "lecteur": "Lecteur (public)"}[role],
        "nav_items": nav,
        "side_card": side_card,
        "all_users": User.query.order_by(User.nom).all(),
        "nb_campagnes_en_cours": nb_campagnes_en_cours,
        "spaces": accessible_spaces(),
        "current_space": space,
        "nav_heading": {"repondant": "Mon espace", "pilote": "Pilotage",
                        "lecteur": "Restitution"}[space],
    }


# ──────────────────────────────────────────────
# Accueil (par rôle)
# ──────────────────────────────────────────────

@app.route("/")
def home():
    space = current_space()
    if space == "repondant":
        return redirect(url_for("mes_evaluations"))
    if space == "lecteur":
        return redirect(url_for("restitution"))
    return pilote_dashboard()


def pilote_dashboard():
    """Tableau de bord pilote (P_HOME)."""
    ref = ReferentielVersion.query.filter_by(is_active=True).first() or ReferentielVersion.query.first()

    kpis = {
        "organisations": Entite.query.count(),
        "sites": Site.query.count(),
        "referentiels": ReferentielVersion.query.count(),
        "validees": Evaluation.query.filter_by(statut="validee").count(),
        "campagnes": Campagne.query.count(),
    }

    # Score moyen global (org, dernière éval validée par entité/ref actif)
    org_evals = Evaluation.query.filter(Evaluation.statut == "validee",
                                        Evaluation.entite_id.isnot(None)).all()
    moyennes = [global_score(ev) for ev in org_evals]
    kpis["score_moyen"] = round(sum(moyennes) / len(moyennes), 1) if moyennes else 0

    campagne = Campagne.query.filter_by(statut="en_cours").order_by(Campagne.date_debut.desc()).first()
    camp_data = None
    if campagne:
        camp_data = {"campagne": campagne, "stats": campagne_stats(campagne)}

    # Radar moyen + classement (sur le référentiel de la campagne courante, sinon actif)
    radar_ref = (campagne.referentiel if campagne and campagne.referentiel_id else ref)
    radar_rows, classement = [], []
    if radar_ref:
        validated = Evaluation.query.filter(
            Evaluation.statut == "validee",
            Evaluation.referentiel_id == radar_ref.id,
            Evaluation.entite_id.isnot(None)).all()
        latest = {}
        for ev in sorted(validated, key=lambda e: e.date_evaluation):
            latest[ev.entite_id] = ev
        dim_totals = {}
        for ev in latest.values():
            for d in compute_scores_by_dimension(ev).values():
                dim_totals.setdefault((d["numero"], d["nom"]), []).append(d["moyenne"])
        radar_rows = [{"dimension": f"{num}. {nom}", "score": round(sum(v) / len(v), 2)}
                      for (num, nom), v in sorted(dim_totals.items())]
        max_niv = get_max_niveau(radar_ref)
        for ev in latest.values():
            score = global_score(ev)
            pct = round(score / max_niv * 100)
            classement.append({"nom": ev.entite.nom, "score": score,
                               "pct": pct, "color": score_color(pct)})
        classement.sort(key=lambda x: -x["score"])

    return render_template("index.html",
        kpis=kpis, camp_data=camp_data,
        radar_ref=radar_ref, radar_rows=radar_rows, classement=classement,
        max_niveau=get_max_niveau(radar_ref) if radar_ref else 4,
    )


# ──────────────────────────────────────────────
# Espace répondant
# ──────────────────────────────────────────────

@app.route("/mes-evaluations")
def mes_evaluations():
    evals = scoped_evaluations_query().order_by(Evaluation.date_evaluation.desc()).all()
    drafts = [eval_summary(e) for e in evals if e.statut == "brouillon"]
    valides = [eval_summary(e) for e in evals if e.statut == "validee"]

    # Invitations en attente : participations de campagnes en cours sans évaluation
    user = current_user()
    invitations = []
    parts = CampagneParticipant.query.join(Campagne).filter(Campagne.statut == "en_cours")
    if user and user.scope_type == "entite" and user.scope_entite_id:
        parts = parts.filter(CampagneParticipant.entite_id == user.scope_entite_id)
    elif user and user.scope_type == "site":
        parts = parts.filter(False)
    for p in parts.all():
        existing = Evaluation.query.filter_by(campagne_id=p.campagne_id, entite_id=p.entite_id).first()
        if not existing:
            invitations.append(p)

    return render_template("mes_evaluations.html",
                           drafts=drafts, valides=valides, invitations=invitations)


@app.route("/evaluation/new", methods=["GET", "POST"])
def evaluation_new():
    referentiels = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    campagnes = Campagne.query.filter_by(statut="en_cours").order_by(Campagne.date_debut.desc()).all()
    entites = Entite.query.order_by(Entite.nom).all()
    sites = Site.query.order_by(Site.nom).all()
    user = current_user()

    # Restriction de périmètre pour un répondant à droit limité
    if user and user.scope_type == "entite" and user.scope_entite_id:
        entites = [e for e in entites if e.id == user.scope_entite_id]
        sites = [s for s in sites if s.organisation_id == user.scope_entite_id]
    elif user and user.scope_type == "site" and user.scope_site_id:
        entites = []
        sites = [s for s in sites if s.id == user.scope_site_id]

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

        # Anti-doublon explicite (la contrainte DB seule ne suffit pas)
        dup = Evaluation.query.filter_by(
            referentiel_id=ref.id,
            campagne_id=eval_kwargs.get("campagne_id"),
            entite_id=eval_kwargs.get("entite_id"),
            site_id=eval_kwargs.get("site_id"),
        ).first()
        if dup:
            flash("Cette évaluation existe déjà (même cible, même référentiel, même campagne) — "
                  "vous avez été redirigé·e vers elle.", "info")
            if dup.statut == "validee":
                return redirect(url_for("evaluation_results", evaluation_id=dup.id))
            return redirect(url_for("evaluation_fill", evaluation_id=dup.id))

        evaluation = Evaluation(**eval_kwargs)
        db.session.add(evaluation)
        db.session.commit()
        return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))

    return render_template("evaluation_new.html",
        referentiels=referentiels, campagnes=campagnes,
        entites=entites, sites=sites,
        preselect={
            "referentiel_id": request.args.get("referentiel_id", type=int),
            "campagne_id": request.args.get("campagne_id", type=int),
            "entite_id": request.args.get("entite_id", type=int),
            "site_id": request.args.get("site_id", type=int),
        },
        evaluateur_default=(user.nom if user else ""),
    )


@app.route("/invitation/<int:campagne_id>/<int:entite_id>")
def invitation(campagne_id, entite_id):
    """Lien d'invitation : pré-remplit le triplet et ouvre le questionnaire."""
    campagne = Campagne.query.get_or_404(campagne_id)
    entite = Entite.query.get_or_404(entite_id)
    ref = campagne.referentiel
    if not ref:
        flash("Cette campagne n'a pas de référentiel attribué — choisissez-le ci-dessous.", "info")
        return redirect(url_for("evaluation_new", campagne_id=campagne.id, entite_id=entite.id))
    if ref.cible != "organisation":
        return redirect(url_for("evaluation_new", campagne_id=campagne.id, referentiel_id=ref.id))

    existing = Evaluation.query.filter_by(
        campagne_id=campagne.id, entite_id=entite.id, referentiel_id=ref.id).first()
    if existing:
        if existing.statut == "validee":
            return redirect(url_for("evaluation_results", evaluation_id=existing.id))
        return redirect(url_for("evaluation_fill", evaluation_id=existing.id))

    user = current_user()
    evaluation = Evaluation(referentiel_id=ref.id, campagne_id=campagne.id,
                            entite_id=entite.id, evaluateur=user.nom if user else "")
    db.session.add(evaluation)
    db.session.commit()
    flash(f"Évaluation de « {entite.nom} » créée pour la campagne « {campagne.label} ».", "success")
    return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))


@app.route("/evaluations")
def evaluations_list():
    evaluations = Evaluation.query.order_by(Evaluation.date_evaluation.desc()).all()
    return render_template("evaluations.html",
                           evaluations=[eval_summary(e) for e in evaluations])


@app.route("/evaluations/<int:evaluation_id>/delete", methods=["POST"])
def evaluation_delete(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    cible_nom = evaluation.cible_nom
    ctx = evaluation.campagne.label if evaluation.campagne_id else "déclaration"
    db.session.delete(evaluation)
    db.session.commit()
    flash(f"Évaluation de « {cible_nom} » ({ctx}) supprimée.", "success")
    return redirect(request.form.get("next") or url_for("evaluations_list"))


@app.route("/evaluation/<int:evaluation_id>/fill", methods=["GET", "POST"])
def evaluation_fill(evaluation_id):
    """Questionnaire — niveau par capacité, non-applicable, justification."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    ref = evaluation.referentiel
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()
    existing_scores = {s.capacite_id: s for s in evaluation.scores}

    if request.method == "POST":
        for dim in dimensions:
            for cap in dim.capacites:
                raw = request.form.get(f"cap_{cap.id}", "")
                justification = request.form.get(f"just_{cap.id}", "").strip()
                if raw == "":
                    # Réponse retirée → supprimer le score existant
                    if cap.id in existing_scores:
                        db.session.delete(existing_scores[cap.id])
                    continue
                niveau_val = 0 if raw == "na" else int(raw)
                if cap.id in existing_scores:
                    existing_scores[cap.id].niveau = niveau_val
                    existing_scores[cap.id].justification = justification
                else:
                    db.session.add(Score(evaluation_id=evaluation.id, capacite_id=cap.id,
                                         niveau=niveau_val, justification=justification))
        db.session.commit()

        action = request.form.get("action", "save")
        if action == "recap":
            return redirect(url_for("evaluation_recap", evaluation_id=evaluation.id))
        flash("Brouillon sauvegardé.", "info")
        return redirect(url_for("evaluation_fill", evaluation_id=evaluation.id))

    done, total = eval_progress(evaluation)
    return render_template("evaluation_fill.html",
        evaluation=evaluation, dimensions=dimensions,
        existing_scores=existing_scores,
        done=done, total=total,
        max_niveau=get_max_niveau(ref),
    )


@app.route("/evaluation/<int:evaluation_id>/recap")
def evaluation_recap(evaluation_id):
    """Vérification avant validation (R_RECAP)."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    if evaluation.statut == "validee":
        return redirect(url_for("evaluation_results", evaluation_id=evaluation.id))
    done, total = eval_progress(evaluation)
    dimensions = Dimension.query.filter_by(referentiel_id=evaluation.referentiel_id) \
        .order_by(Dimension.numero).all()
    missing = []
    for dim in dimensions:
        for cap in dim.capacites:
            if cap.id not in {s.capacite_id for s in evaluation.scores}:
                missing.append(cap)
    dim_scores = compute_scores_by_dimension(evaluation)
    max_niv = get_max_niveau(evaluation.referentiel)
    recap_dims = [{"nom": d["nom"], "moyenne": d["moyenne"],
                   "pct": round(d["moyenne"] / max_niv * 100),
                   "color": score_color(round(d["moyenne"] / max_niv * 100))}
                  for d in dim_scores.values()]
    return render_template("evaluation_recap.html",
        evaluation=evaluation, done=done, total=total, missing=missing,
        recap_dims=recap_dims, max_niveau=max_niv,
    )


@app.route("/evaluation/<int:evaluation_id>/validate", methods=["POST"])
def evaluation_validate(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    done, total = eval_progress(evaluation)
    if done < total:
        flash(f"Validation impossible : {total - done} capacité(s) non renseignée(s).", "error")
        return redirect(url_for("evaluation_recap", evaluation_id=evaluation.id))
    evaluation.statut = "validee"
    evaluation.date_evaluation = datetime.utcnow()
    db.session.commit()
    flash("Évaluation validée — voici vos résultats.", "success")
    return redirect(url_for("evaluation_results", evaluation_id=evaluation.id))


@app.route("/evaluation/<int:evaluation_id>/reopen", methods=["POST"])
def evaluation_reopen(evaluation_id):
    """Réouverture d'une évaluation validée (action pilote)."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    evaluation.statut = "brouillon"
    db.session.commit()
    flash(f"Évaluation de « {evaluation.cible_nom} » repassée en brouillon.", "success")
    return redirect(request.form.get("next") or url_for("evaluation_fill", evaluation_id=evaluation.id))


@app.route("/evaluation/<int:evaluation_id>/results")
def evaluation_results(evaluation_id):
    """Résultats d'une évaluation — lecture simple + vue experte."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    ref = evaluation.referentiel
    dim_scores = compute_scores_by_dimension(evaluation)
    max_niveau = get_max_niveau(ref)
    score = global_score(evaluation)
    pct = round(score / max_niveau * 100) if max_niveau else 0

    # Niveau global nommé (niveau entier le plus proche)
    niveau_names = {}
    for dim in ref.dimensions:
        for cap in dim.capacites:
            for niv in cap.niveaux:
                niveau_names.setdefault(niv.niveau, niv.nom)
            break
        break
    niveau_name = niveau_names.get(round(score), "")

    # Détail par capacité (avec NA)
    detail = []
    for s in evaluation.scores:
        cap = s.capacite
        detail.append({
            "dimension": cap.dimension.nom, "dim_numero": cap.dimension.numero,
            "capacite": cap.nom, "cap_numero": cap.numero, "portee": cap.portee,
            "niveau": s.niveau,
            "niveau_nom": next((n.nom for n in cap.niveaux if n.niveau == s.niveau), "Non applicable"),
            "justification": s.justification or "",
        })
    detail.sort(key=lambda x: (x["dim_numero"], [int(p) for p in str(x["cap_numero"]).split(".") if p.isdigit()]))

    # Les 3 choses à retenir : point fort, point faible, prochaine étape
    dims_sorted = sorted(dim_scores.values(), key=lambda d: -d["moyenne"])
    takeaways = {}
    if dims_sorted:
        takeaways["fort"] = dims_sorted[0]
        takeaways["faible"] = dims_sorted[-1]
    low_caps = [d for d in detail if 0 < d["niveau"] < max_niveau]
    if low_caps:
        weakest = min(low_caps, key=lambda d: d["niveau"])
        next_niv = next((n for n in Capacite.query
                         .filter_by(numero=weakest["cap_numero"])
                         .join(Dimension).filter(Dimension.referentiel_id == ref.id)
                         .first().niveaux if n.niveau == weakest["niveau"] + 1), None)
        takeaways["next"] = {"cap": weakest, "action": next_niv.description if next_niv else ""}

    # Évolution vs précédente évaluation validée (même cible, même ref)
    prev_q = Evaluation.query.filter(
        Evaluation.statut == "validee",
        Evaluation.referentiel_id == ref.id,
        Evaluation.id != evaluation.id,
        Evaluation.date_evaluation < evaluation.date_evaluation)
    if evaluation.entite_id:
        prev_q = prev_q.filter_by(entite_id=evaluation.entite_id)
    else:
        prev_q = prev_q.filter_by(site_id=evaluation.site_id)
    prev = prev_q.order_by(Evaluation.date_evaluation.desc()).first()
    delta_pts = None
    if prev:
        prev_pct = round(global_score(prev) / max_niveau * 100)
        delta_pts = pct - prev_pct

    radar_rows = [{"dimension": f"{d['numero']}. {d['nom']}", "score": d["moyenne"]}
                  for d in dim_scores.values()]

    return render_template("evaluation_results.html",
        evaluation=evaluation, dim_scores=dim_scores, detail=detail,
        score=score, pct=pct, color=score_color(pct), niveau_name=niveau_name,
        takeaways=takeaways, delta_pts=delta_pts,
        radar_rows=radar_rows, max_niveau=max_niveau,
    )


# ──────────────────────────────────────────────
# Référentiel (consultation partagée)
# ──────────────────────────────────────────────

@app.route("/referentiel")
def referentiel_view():
    ref_id = request.args.get("ref_id", type=int)
    if ref_id:
        ref = ReferentielVersion.query.get_or_404(ref_id)
    else:
        ref = ReferentielVersion.query.filter_by(is_active=True).first() or ReferentielVersion.query.first()

    all_refs = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all()

    all_validated = Evaluation.query.filter_by(statut="validee", referentiel_id=ref.id).all()
    cap_avg, cap_counts = {}, {}
    for ev in all_validated:
        for s in scored(ev.scores):
            cap_avg[s.capacite_id] = cap_avg.get(s.capacite_id, 0) + s.niveau
            cap_counts[s.capacite_id] = cap_counts.get(s.capacite_id, 0) + 1
    cap_averages = {cid: round(total / cap_counts[cid], 1) for cid, total in cap_avg.items()}

    # Échelle : niveaux de la 1re capacité (pédagogie)
    scale = []
    for dim in dimensions:
        if dim.capacites and dim.capacites[0].niveaux:
            scale = dim.capacites[0].niveaux
            break

    return render_template("referentiel.html",
        referentiel=ref, dimensions=dimensions, cap_averages=cap_averages,
        nb_evaluations=len(all_validated),
        nb_capacites=sum(len(d.capacites) for d in dimensions),
        all_refs=all_refs, current_ref_id=ref.id,
        max_niveau=get_max_niveau(ref), scale=scale,
    )


# ──────────────────────────────────────────────
# Espace pilote — campagnes
# ──────────────────────────────────────────────

@app.route("/campagnes")
@require_roles("pilote", "admin")
def campagnes_list():
    campagnes = Campagne.query.order_by(Campagne.date_debut.desc()).all()
    rows = [{"campagne": c, "stats": campagne_stats(c)} for c in campagnes]
    return render_template("campagnes.html", rows=rows)


@app.route("/campagnes/new", methods=["GET", "POST"])
@require_roles("pilote", "admin")
def campagne_new():
    referentiels = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    if request.method == "POST":
        campagne = Campagne(
            label=request.form["label"],
            date_debut=date.fromisoformat(request.form["date_debut"]),
            date_fin=date.fromisoformat(request.form["date_fin"]) if request.form.get("date_fin") else None,
            referentiel_id=int(request.form["referentiel_id"]) if request.form.get("referentiel_id") else None,
        )
        db.session.add(campagne)
        db.session.commit()
        flash(f"Campagne « {campagne.label} » créée — définissez son périmètre.", "success")
        return redirect(url_for("campagne_detail", campagne_id=campagne.id, tab="perimetre"))
    return render_template("campagne_form.html", referentiels=referentiels)


@app.route("/campagne/<int:campagne_id>")
@require_roles("pilote", "admin")
def campagne_detail(campagne_id):
    """Détail campagne à onglets : suivi / périmètre / invitations / réglages."""
    campagne = Campagne.query.get_or_404(campagne_id)
    tab = request.args.get("tab", "suivi")
    stats = campagne_stats(campagne)
    entites = Entite.query.order_by(Entite.nom).all()
    participant_ids = {p.entite_id for p in campagne.participants}
    referentiels = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    return render_template("campagne_detail.html",
        campagne=campagne, stats=stats, tab=tab,
        entites=entites, participant_ids=participant_ids,
        referentiels=referentiels,
    )


@app.route("/campagne/<int:campagne_id>/perimetre", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_perimetre(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    selected = {int(x) for x in request.form.getlist("entite_ids") if x.isdigit()}
    existing = {p.entite_id: p for p in campagne.participants}
    for eid, p in existing.items():
        if eid not in selected:
            db.session.delete(p)
    for eid in selected:
        if eid not in existing:
            db.session.add(CampagneParticipant(campagne_id=campagne.id, entite_id=eid))
    db.session.commit()
    flash(f"Périmètre enregistré ({len(selected)} entités attendues).", "success")
    return redirect(url_for("campagne_detail", campagne_id=campagne.id, tab="suivi"))


@app.route("/campagne/<int:campagne_id>/update", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_update(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    campagne.label = request.form.get("label", campagne.label)
    if request.form.get("date_debut"):
        campagne.date_debut = date.fromisoformat(request.form["date_debut"])
    campagne.date_fin = date.fromisoformat(request.form["date_fin"]) if request.form.get("date_fin") else None
    if request.form.get("referentiel_id"):
        campagne.referentiel_id = int(request.form["referentiel_id"])
    db.session.commit()
    flash("Campagne mise à jour.", "success")
    return redirect(url_for("campagne_detail", campagne_id=campagne.id, tab="reglages"))


@app.route("/campagne/<int:campagne_id>/statut", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_statut(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    if campagne.statut == "en_cours":
        campagne.statut = "terminee"
        flash(f"Campagne « {campagne.label} » clôturée — les résultats sont figés.", "success")
    else:
        campagne.statut = "en_cours"
        flash(f"Campagne « {campagne.label} » réouverte.", "success")
    db.session.commit()
    return redirect(url_for("campagne_detail", campagne_id=campagne.id, tab="reglages"))


def _invitation_link(campagne, entite):
    if campagne.referentiel and campagne.referentiel.cible == "organisation":
        return url_for("invitation", campagne_id=campagne.id, entite_id=entite.id, _external=True)
    return url_for("evaluation_new", campagne_id=campagne.id, entite_id=entite.id, _external=True)


def _send_relance(campagne, entite, invitation=False):
    """Envoie une relance (ou invitation) à l'email de contact d'une entité."""
    if not entite.email_contact:
        raise mailer.MailerError(f"« {entite.nom} » n'a pas d'email de contact")
    lien = _invitation_link(campagne, entite)
    if invitation:
        sujet = f"Invitation — {campagne.label}"
        titre = "Invitation à vous auto-évaluer"
        corps = (f"<p>Bonjour,</p><p>Dans le cadre de la campagne <strong>{campagne.label}</strong>, "
                 f"vous êtes invité·e à renseigner l'auto-évaluation de <strong>{entite.nom}</strong> "
                 f"sur le référentiel {campagne.referentiel.label if campagne.referentiel else ''}. "
                 f"Le lien ci-dessous pré-remplit tout : vous n'avez plus qu'à répondre. "
                 f"Vous pouvez interrompre et reprendre à tout moment.</p>")
    else:
        sujet = f"Relance — {campagne.label}"
        titre = "Votre évaluation est attendue"
        corps = (f"<p>Bonjour,</p><p>L'auto-évaluation de <strong>{entite.nom}</strong> pour la campagne "
                 f"<strong>{campagne.label}</strong> n'est pas encore validée"
                 + (f" (échéance le {campagne.date_fin.strftime('%d/%m/%Y')})" if campagne.date_fin else "")
                 + ".</p><p>Le lien ci-dessous vous amène directement à votre questionnaire.</p>")
    texte = (f"Bonjour,\n\n{'Invitation à vous auto-évaluer' if invitation else 'Votre évaluation est attendue'} — "
             f"{campagne.label} · {entite.nom}.\n\nLien direct : {lien}\n")
    mailer.send(entite.email_contact, sujet, texte, titre=titre, corps_html=corps,
                lien=lien, lien_label="Ouvrir mon évaluation")


@app.route("/campagne/<int:campagne_id>/relancer/<int:entite_id>", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_relancer(campagne_id, entite_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    entite = Entite.query.get_or_404(entite_id)
    invitation = request.form.get("mode") == "invitation"
    try:
        _send_relance(campagne, entite, invitation=invitation)
        flash(f"{'Invitation' if invitation else 'Relance'} envoyée à {entite.email_contact} "
              f"({entite.nom}).", "success")
    except mailer.MailerError as e:
        flash(f"Envoi impossible : {e}.", "error")
    return redirect(url_for("campagne_detail", campagne_id=campagne.id,
                            tab="invitations" if invitation else "suivi"))


@app.route("/campagne/<int:campagne_id>/relancer-tous", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_relancer_tous(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    stats = campagne_stats(campagne)
    envoyees, sans_adresse, erreurs = 0, [], []
    for r in stats["rows"]:
        if r["statut"] == "validee" or not r.get("entite"):
            continue
        try:
            _send_relance(campagne, r["entite"])
            envoyees += 1
        except mailer.MailerError as e:
            (sans_adresse if "email de contact" in str(e) else erreurs).append(r["entite"].nom)
    msg = f"{envoyees} relance{'s' if envoyees > 1 else ''} envoyée{'s' if envoyees > 1 else ''}."
    if sans_adresse:
        msg += f" Sans adresse de contact : {', '.join(sans_adresse)}."
    if erreurs:
        msg += f" Échec d'envoi : {', '.join(erreurs)}."
    flash(msg, "error" if erreurs else ("warning" if sans_adresse else "success"))
    return redirect(url_for("campagne_detail", campagne_id=campagne.id, tab="suivi"))


@app.route("/campagnes/<int:campagne_id>/delete", methods=["POST"])
@require_roles("pilote", "admin")
def campagne_delete(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    label = campagne.label
    db.session.delete(campagne)
    db.session.commit()
    flash(f"Campagne « {label} » supprimée (évaluations et scores inclus).", "success")
    return redirect(url_for("campagnes_list"))


def campagne_dashboard_data(campagne):
    """Radar comparatif, stats par dimension et heatmap d'une campagne."""
    validated = Evaluation.query.filter_by(campagne_id=campagne.id, statut="validee").all()
    stats = compute_global_stats(campagne)
    ref = campagne.referentiel or (validated[0].referentiel if validated else None)
    dimensions = Dimension.query.filter_by(referentiel_id=ref.id).order_by(Dimension.numero).all() if ref else []
    max_niveau = get_max_niveau(ref) if ref else 4

    # Radar : série « Moyenne » + une série par entité (tidy pour series-field)
    radar_rows = []
    if stats:
        for s in stats.values():
            radar_rows.append({"dimension": f"{s['numero']}. {s['nom']}",
                               "serie": "Moyenne", "score": s["moyenne"]})
    for ev in validated:
        for d in compute_scores_by_dimension(ev).values():
            radar_rows.append({"dimension": f"{d['numero']}. {d['nom']}",
                               "serie": ev.cible_nom, "score": d["moyenne"]})

    # Stats enrichies pour le tableau
    dim_stats = []
    if stats:
        for s in stats.values():
            pct = round(s["moyenne"] / max_niveau * 100)
            dim_stats.append({**s, "pct": pct, "color": score_color(pct)})

    # Heatmap entités × capacités
    all_capacites = [cap for dim in dimensions for cap in dim.capacites]
    heatmap = []
    for ev in validated:
        cell = {s.capacite_id: s for s in ev.scores}
        heatmap.append({"nom": ev.cible_nom,
                        "cells": [cell.get(c.id) for c in all_capacites]})

    return {
        "campagne": campagne, "stats_campagne": campagne_stats(campagne),
        "referentiel": ref, "dimensions": dimensions, "all_capacites": all_capacites,
        "radar_rows": radar_rows, "dim_stats": dim_stats, "heatmap": heatmap,
        "max_niveau": max_niveau, "nb_validees": len(validated),
    }


def campagne_synthese(campagne):
    """Messages exécutifs d'une campagne (progression, chantier, entité qui décroche, fiabilité)."""
    validated = Evaluation.query.filter_by(campagne_id=campagne.id, statut="validee").all()
    ref = campagne.referentiel or (validated[0].referentiel if validated else None)
    max_niveau = get_max_niveau(ref) if ref else 4
    stats = compute_global_stats(campagne)
    camp_part = campagne_stats(campagne)

    scores = [global_score(ev) for ev in validated]
    score_moyen = round(sum(scores) / len(scores), 2) if scores else 0
    pct_moyen = round(score_moyen / max_niveau * 100)
    delta = prev_label = None
    if ref:
        for c in Campagne.query.filter(Campagne.id != campagne.id,
                                       Campagne.date_debut < campagne.date_debut) \
                .order_by(Campagne.date_debut.desc()).all():
            c_evals = [ev for ev in c.evaluations
                       if ev.statut == "validee" and ev.referentiel_id == ref.id]
            if c_evals:
                prev_scores = [global_score(ev) for ev in c_evals]
                prev_pct = round(sum(prev_scores) / len(prev_scores) / max_niveau * 100)
                delta = pct_moyen - prev_pct
                prev_label = c.label
                break

    weakest_dim = min(stats.values(), key=lambda s: s["moyenne"]) if stats else None
    classement = []
    for ev in validated:
        s = global_score(ev)
        p = round(s / max_niveau * 100)
        classement.append({"nom": ev.cible_nom, "entite_id": ev.entite_id,
                           "score": s, "pct": p, "color": score_color(p)})
    classement.sort(key=lambda x: -x["score"])
    weakest_entity = classement[-1] if classement else None

    all_scores = [s for ev in validated for s in scored(ev.scores)]
    justif_pct = round(100 * sum(1 for s in all_scores if (s.justification or "").strip())
                       / len(all_scores)) if all_scores else 0
    refs_used = {ev.referentiel_id for ev in validated}

    return {
        "referentiel": ref, "max_niveau": max_niveau,
        "score_moyen": score_moyen, "pct_moyen": pct_moyen,
        "delta": delta, "prev_label": prev_label,
        "weakest_dim": weakest_dim, "weakest_entity": weakest_entity,
        "classement": classement, "camp_part": camp_part,
        "justif_pct": justif_pct, "ref_partage": (len(refs_used) == 1),
    }


@app.route("/campagne/<int:campagne_id>/dashboard")
def campagne_dashboard(campagne_id):
    """Restitution campagne : radar comparatif, stats par dimension, heatmap."""
    campagne = Campagne.query.get_or_404(campagne_id)
    return render_template("campagne_dashboard.html", **campagne_dashboard_data(campagne))


@app.route("/campagne/<int:campagne_id>/rapport")
def campagne_rapport(campagne_id):
    """Rapport de restitution — page dédiée, optimisée impression/PDF (COPIL)."""
    campagne = Campagne.query.get_or_404(campagne_id)
    data = campagne_dashboard_data(campagne)
    data["synthese"] = campagne_synthese(campagne)
    return render_template("rapport.html", **data)


# ──────────────────────────────────────────────
# Espace pilote — patrimoine (organisations, sites)
# ──────────────────────────────────────────────

@app.route("/entites")
@require_roles("pilote", "admin")
def entites_list():
    entites = Entite.query.order_by(Entite.nom).all()
    entite_scores = {e.id: target_scores_summary(entite_id=e.id) for e in entites}
    return render_template("entites.html", entites=entites, entite_scores=entite_scores)


@app.route("/entites/new", methods=["GET", "POST"])
@app.route("/entites/<int:entite_id>/edit", methods=["GET", "POST"])
@require_roles("pilote", "admin")
def entite_form(entite_id=None):
    entite = Entite.query.get_or_404(entite_id) if entite_id else None
    if request.method == "POST":
        if entite is None:
            entite = Entite(nom="", type="Bureau")
            db.session.add(entite)
        entite.nom = request.form["nom"]
        entite.type = request.form["type"]
        entite.direction = request.form.get("direction", "")
        entite.email_contact = request.form.get("email_contact", "").strip()
        entite.description = request.form.get("description", "")
        db.session.commit()
        flash(f"Organisation « {entite.nom} » enregistrée.", "success")
        return redirect(url_for("entites_list"))
    return render_template("entite_form.html", entite=entite)


@app.route("/entites/<int:entite_id>/delete", methods=["POST"])
@require_roles("pilote", "admin")
def entite_delete(entite_id):
    entite = Entite.query.get_or_404(entite_id)
    nom = entite.nom
    for evaluation in entite.evaluations:
        db.session.delete(evaluation)
    db.session.delete(entite)
    db.session.commit()
    flash(f"Organisation « {nom} » supprimée (évaluations incluses).", "success")
    return redirect(url_for("entites_list"))


@app.route("/sites")
@require_roles("pilote", "admin")
def sites_list():
    sites = Site.query.order_by(Site.nom).all()
    site_scores = {s.id: target_scores_summary(site_id=s.id) for s in sites}
    return render_template("sites.html", sites=sites, site_scores=site_scores)


@app.route("/sites/new", methods=["GET", "POST"])
@app.route("/sites/<int:site_id>/edit", methods=["GET", "POST"])
@require_roles("pilote", "admin")
def site_form(site_id=None):
    site = Site.query.get_or_404(site_id) if site_id else None
    entites = Entite.query.order_by(Entite.nom).all()
    if request.method == "POST":
        if site is None:
            site = Site(nom="", organisation_id=int(request.form["organisation_id"]))
            db.session.add(site)
        site.nom = request.form["nom"]
        site.url = request.form.get("url", "")
        site.description = request.form.get("description", "")
        site.organisation_id = int(request.form["organisation_id"])
        db.session.commit()
        flash(f"Site « {site.nom} » enregistré.", "success")
        return redirect(url_for("sites_list"))
    return render_template("site_form.html", site=site, entites=entites)


@app.route("/sites/<int:site_id>/delete", methods=["POST"])
@require_roles("pilote", "admin")
def site_delete(site_id):
    site = Site.query.get_or_404(site_id)
    nom = site.nom
    for evaluation in site.evaluations:
        db.session.delete(evaluation)
    db.session.delete(site)
    db.session.commit()
    flash(f"Site « {nom} » supprimé (évaluations incluses).", "success")
    return redirect(url_for("sites_list"))


# ──────────────────────────────────────────────
# Espace pilote — référentiels & utilisateurs
# ──────────────────────────────────────────────

@app.route("/referentiels")
@require_roles("pilote", "admin")
def referentiels_admin():
    refs = ReferentielVersion.query.order_by(ReferentielVersion.label).all()
    rows = []
    for r in refs:
        nb_dims, nb_caps = ref_counts(r)
        rows.append({
            "ref": r, "nb_dims": nb_dims, "nb_caps": nb_caps,
            "max_niveau": get_max_niveau(r),
            "nb_evals": Evaluation.query.filter_by(referentiel_id=r.id).count(),
        })
    return render_template("referentiels.html", rows=rows)


@app.route("/referentiels/<int:ref_id>/toggle", methods=["POST"])
@require_roles("pilote", "admin")
def referentiel_toggle(ref_id):
    ref = ReferentielVersion.query.get_or_404(ref_id)
    ref.is_active = not ref.is_active
    db.session.commit()
    flash(f"Référentiel « {ref.label} » {'activé' if ref.is_active else 'désactivé'}.", "success")
    return redirect(url_for("referentiels_admin"))


def create_referentiel_from_data(data):
    """Crée un référentiel depuis la structure commune JSON/xlsx. Retourne le référentiel."""
    label = data["label"]
    if ReferentielVersion.query.filter_by(label=label).first():
        raise ValueError(f"un référentiel « {label} » existe déjà — changez le label "
                         "(un référentiel utilisé ne peut pas être modifié en place)")
    ref = ReferentielVersion(
        label=label,
        description=data.get("description", ""),
        cible=data.get("cible", "organisation"),
        is_active=False,
    )
    db.session.add(ref)
    db.session.flush()
    for dim_data in data["dimensions"]:
        dim = Dimension(referentiel_id=ref.id, numero=int(dim_data["numero"]),
                        nom=dim_data["nom"], description=dim_data.get("description", ""))
        db.session.add(dim)
        db.session.flush()
        for cap_data in dim_data["capacites"]:
            cap = Capacite(dimension_id=dim.id, numero=str(cap_data["numero"]),
                           nom=cap_data["nom"], description=cap_data.get("description", ""),
                           portee=cap_data.get("portee", "P"))
            db.session.add(cap)
            db.session.flush()
            for niv_data in cap_data["niveaux"]:
                db.session.add(NiveauCritere(
                    capacite_id=cap.id, niveau=int(niv_data["niveau"]),
                    nom=niv_data["nom"], description=niv_data["description"],
                    signaux_observables=niv_data.get("signaux_observables", "")))
    db.session.commit()
    return ref


@app.route("/referentiels/import", methods=["GET", "POST"])
@require_roles("pilote", "admin")
def referentiel_import():
    """Import d'un référentiel — JSON structuré ou tableur xlsx (parseur stdlib)."""
    if request.method == "POST":
        file = request.files.get("fichier")
        if not file or not file.filename:
            flash("Aucun fichier fourni.", "error")
            return redirect(url_for("referentiel_import"))
        fname = file.filename.lower()
        try:
            if fname.endswith(".json"):
                data = json.load(file.stream)
                if request.form.get("cible"):
                    data["cible"] = request.form["cible"]
            elif fname.endswith(".xlsx"):
                from xlsx_import import parse_referentiel_xlsx
                label = (request.form.get("label") or "").strip()
                if not label:
                    flash("Pour un import xlsx, renseignez le label du référentiel "
                          "(ex. Design-org-v2).", "error")
                    return redirect(url_for("referentiel_import"))
                data = parse_referentiel_xlsx(
                    file.stream, label=label,
                    description=request.form.get("description", "").strip(),
                    cible=request.form.get("cible") or "organisation")
            else:
                flash("Format non reconnu : fournir un .json ou un .xlsx.", "warning")
                return redirect(url_for("referentiel_import"))

            ref = create_referentiel_from_data(data)
            nb_dims, nb_caps = ref_counts(ref)
            flash(f"Référentiel « {ref.label} » importé : {nb_dims} dimensions, {nb_caps} capacités. "
                  "Activez-le pour le proposer aux répondants.", "success")
            return redirect(url_for("referentiels_admin"))
        except (KeyError, ValueError, TypeError) as e:
            db.session.rollback()
            flash(f"Fichier invalide : {e}", "error")
            return redirect(url_for("referentiel_import"))
    return render_template("referentiel_import.html")


@app.route("/utilisateurs")
@require_roles("pilote", "admin")
def users_list():
    users = User.query.order_by(User.nom).all()
    entites = Entite.query.order_by(Entite.nom).all()
    sites = Site.query.order_by(Site.nom).all()
    edit_id = request.args.get("edit", type=int)
    return render_template("users.html", users=users, entites=entites,
                           sites=sites, edit_id=edit_id)


@app.route("/utilisateurs/save", methods=["POST"])
@require_roles("pilote", "admin")
def user_save():
    uid = request.form.get("user_id", type=int)
    user = db.session.get(User, uid) if uid else User(nom="", email="")
    user.nom = request.form["nom"]
    user.email = request.form["email"]
    user.role = request.form["role"] if request.form["role"] in User.ROLES else "repondant"
    user.scope_type = request.form["scope_type"] if request.form["scope_type"] in User.SCOPES else "global"
    user.scope_entite_id = request.form.get("scope_entite_id", type=int) if user.scope_type == "entite" else None
    user.scope_site_id = request.form.get("scope_site_id", type=int) if user.scope_type == "site" else None
    if not uid:
        db.session.add(user)
    try:
        db.session.commit()
        flash(f"Utilisateur « {user.nom} » enregistré ({user.role_label} · {user.scope_label}).", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Un compte existe déjà avec cet email.", "error")
    return redirect(url_for("users_list"))


@app.route("/utilisateurs/<int:user_id>/delete", methods=["POST"])
@require_roles("pilote", "admin")
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if session.get("user_id") == user.id:
        session.pop("user_id", None)
    nom = user.nom
    db.session.delete(user)
    db.session.commit()
    flash(f"Compte « {nom} » supprimé.", "success")
    return redirect(url_for("users_list"))


# ──────────────────────────────────────────────
# Espace lecteur (public)
# ──────────────────────────────────────────────

def campagnes_with_results():
    out = []
    for c in Campagne.query.order_by(Campagne.date_debut.desc()).all():
        if any(ev.statut == "validee" for ev in c.evaluations):
            out.append(c)
    return out


@app.route("/restitution")
def restitution():
    """Vue d'ensemble exécutive (L_HOME)."""
    campagnes = campagnes_with_results()
    campagne_id = request.args.get("campagne_id", type=int)
    campagne = None
    if campagne_id:
        campagne = Campagne.query.get_or_404(campagne_id)
    elif campagnes:
        campagne = campagnes[0]

    if not campagne:
        return render_template("restitution.html", campagne=None, campagnes=campagnes)

    return render_template("restitution.html",
        campagne=campagne, campagnes=campagnes, **campagne_synthese(campagne))


def sites_consolidation(entite):
    """Consolidation sites → organisation (issue #5).

    Règle : par référentiel « site », moyenne simple des scores globaux des
    dernières évaluations validées des sites rattachés à l'organisation.
    """
    agg = {}
    for site in entite.sites:
        for card in target_scores_summary(site_id=site.id):
            a = agg.setdefault(card["ref"].id, {"ref": card["ref"], "max": card["max"], "scores": []})
            a["scores"].append(card["score"])
    out = []
    for a in agg.values():
        score = round(sum(a["scores"]) / len(a["scores"]), 2)
        pct = round(score / a["max"] * 100) if a["max"] else 0
        out.append({"ref": a["ref"], "score": score, "max": a["max"], "pct": pct,
                    "color": score_color(pct), "nb_sites": len(a["scores"])})
    out.sort(key=lambda x: x["ref"].label)
    return out


@app.route("/restitution/organisation")
@app.route("/restitution/organisation/<int:entite_id>")
def restitution_orgs(entite_id=None):
    """Fiche organisation (L_ENTITY)."""
    entites = Entite.query.order_by(Entite.nom).all()
    entite = Entite.query.get_or_404(entite_id) if entite_id else (entites[0] if entites else None)
    if not entite:
        return render_template("restitution_entite.html", entite=None, entites=entites)

    ref_cards = target_scores_summary(entite_id=entite.id)

    # Radar : dernière évaluation validée du référentiel « préféré » (actif sinon 1er)
    radar_eval = None
    for card in ref_cards:
        if card["ref"].is_active:
            radar_eval = card["eval"]
            break
    if not radar_eval and ref_cards:
        radar_eval = ref_cards[0]["eval"]
    radar_rows, radar_max = [], 4
    if radar_eval:
        radar_rows = [{"dimension": f"{d['numero']}. {d['nom']}", "score": d["moyenne"]}
                      for d in compute_scores_by_dimension(radar_eval).values()]
        radar_max = get_max_niveau(radar_eval.referentiel)

    sites_rows = []
    for s in entite.sites:
        cards = target_scores_summary(site_id=s.id)
        sites_rows.append({"site": s, "cards": cards})

    return render_template("restitution_entite.html",
        entite=entite, entites=entites, ref_cards=ref_cards,
        radar_eval=radar_eval, radar_rows=radar_rows, radar_max=radar_max,
        sites_rows=sites_rows, consolidation=sites_consolidation(entite),
    )


@app.route("/evolution")
def evolution_view():
    """Évolution dans le temps, avec sélecteur d'organisation (L_EVOLUTION)."""
    entites = [e for e in Entite.query.order_by(Entite.nom).all()
               if Evaluation.query.filter_by(entite_id=e.id, statut="validee").count()]
    entite_id = request.args.get("entite_id", type=int)
    entite = Entite.query.get_or_404(entite_id) if entite_id else (entites[0] if entites else None)
    if not entite:
        return render_template("entite_evolution.html", entite=None, entites=entites, charts=[])
    return entite_evolution_render(entite, entites)


@app.route("/entite/<int:entite_id>/evolution")
def entite_evolution(entite_id):
    entite = Entite.query.get_or_404(entite_id)
    entites = [e for e in Entite.query.order_by(Entite.nom).all()
               if Evaluation.query.filter_by(entite_id=e.id, statut="validee").count()]
    return entite_evolution_render(entite, entites)


def entite_evolution_render(entite, entites):
    evaluations = Evaluation.query.filter_by(entite_id=entite.id, statut="validee") \
        .order_by(Evaluation.date_evaluation).all()

    ref_groups = {}
    for ev in evaluations:
        ref_groups.setdefault(ev.referentiel_id, []).append(ev)

    charts = []
    for ref_id, evs in ref_groups.items():
        ref = evs[0].referentiel
        max_niveau = get_max_niveau(ref)
        # Données tidy : {campagne, dimension, score}
        rows = []
        for ev in evs:
            label = ev.campagne.label if ev.campagne_id else ev.date_evaluation.strftime("%Y-%m-%d")
            for d in compute_scores_by_dimension(ev).values():
                rows.append({"campagne": label, "dimension": f"{d['numero']}. {d['nom']}",
                             "score": d["moyenne"]})
        last = evs[-1]
        radar_rows = [{"dimension": f"{d['numero']}. {d['nom']}", "score": d["moyenne"]}
                      for d in compute_scores_by_dimension(last).values()]
        charts.append({
            "ref": ref, "max_niveau": max_niveau, "nb_evaluations": len(evs),
            "line_rows": rows, "radar_rows": radar_rows,
        })

    return render_template("entite_evolution.html",
                           entite=entite, entites=entites, charts=charts)


@app.route("/comparer")
def comparer():
    """Comparaison 2 organisations ou 2 campagnes (L_COMPARE)."""
    mode = request.args.get("mode", "orgs")
    referentiels = [r for r in ReferentielVersion.query.order_by(ReferentielVersion.label).all()
                    if Evaluation.query.filter_by(referentiel_id=r.id, statut="validee").count()]
    ref_id = request.args.get("ref_id", type=int)
    ref = ReferentielVersion.query.get(ref_id) if ref_id else None
    if not ref and referentiels:
        ref = max(referentiels,
                  key=lambda r: Evaluation.query.filter_by(referentiel_id=r.id, statut="validee").count())
    max_niveau = get_max_niveau(ref) if ref else 4

    ctx = {"mode": mode, "referentiels": referentiels, "ref": ref, "max_niveau": max_niveau,
           "radar_rows": [], "table_rows": [], "a_label": None, "b_label": None}

    if not ref:
        return render_template("comparer.html", **ctx)

    def dims_of(ev):
        return {f"{d['numero']}. {d['nom']}": d["moyenne"]
                for d in compute_scores_by_dimension(ev).values()}

    if mode == "campagnes":
        campagnes = [c for c in Campagne.query.order_by(Campagne.date_debut.desc()).all()
                     if any(ev.statut == "validee" and ev.referentiel_id == ref.id
                            for ev in c.evaluations)]
        ctx["choices"] = campagnes
        a_id = request.args.get("a", type=int) or (campagnes[0].id if campagnes else None)
        b_id = request.args.get("b", type=int) or (campagnes[1].id if len(campagnes) > 1 else None)
        series = {}
        for key, cid in (("a", a_id), ("b", b_id)):
            if not cid:
                continue
            c = Campagne.query.get(cid)
            evs = [ev for ev in c.evaluations if ev.statut == "validee" and ev.referentiel_id == ref.id]
            agg = {}
            for ev in evs:
                for dim, val in dims_of(ev).items():
                    agg.setdefault(dim, []).append(val)
            series[key] = (c.label, {d: round(sum(v) / len(v), 2) for d, v in agg.items()})
        ctx["a_id"], ctx["b_id"] = a_id, b_id
    else:
        entites = [e for e in Entite.query.order_by(Entite.nom).all()
                   if any(ev.referentiel_id == ref.id for ev in e.evaluations if ev.statut == "validee")]
        ctx["choices"] = entites
        a_id = request.args.get("a", type=int) or (entites[0].id if entites else None)
        b_id = request.args.get("b", type=int) or (entites[1].id if len(entites) > 1 else None)
        series = {}
        for key, eid in (("a", a_id), ("b", b_id)):
            if not eid:
                continue
            ev = Evaluation.query.filter_by(entite_id=eid, referentiel_id=ref.id, statut="validee") \
                .order_by(Evaluation.date_evaluation.desc()).first()
            if ev:
                series[key] = (ev.entite.nom, dims_of(ev))
        ctx["a_id"], ctx["b_id"] = a_id, b_id

    if "a" in series:
        ctx["a_label"] = series["a"][0]
    if "b" in series:
        ctx["b_label"] = series["b"][0]
    dims_all = []
    for key in ("a", "b"):
        if key in series:
            for d in series[key][1]:
                if d not in dims_all:
                    dims_all.append(d)
    radar_rows, table_rows = [], []
    for d in dims_all:
        a_val = series.get("a", (None, {}))[1].get(d)
        b_val = series.get("b", (None, {}))[1].get(d)
        if a_val is not None:
            radar_rows.append({"dimension": d, "serie": series["a"][0], "score": a_val})
        if b_val is not None:
            radar_rows.append({"dimension": d, "serie": series["b"][0], "score": b_val})
        delta = round(a_val - b_val, 2) if (a_val is not None and b_val is not None) else None
        table_rows.append({"dimension": d, "a": a_val, "b": b_val, "delta": delta})
    ctx["radar_rows"], ctx["table_rows"] = radar_rows, table_rows

    return render_template("comparer.html", **ctx)


@app.route("/plan-action")
@app.route("/plan-action/<int:entite_id>")
def plan_action(entite_id=None):
    """Plan d'action : le niveau supérieur de chaque capacité faible (L_ACTION)."""
    entites = [e for e in Entite.query.order_by(Entite.nom).all()
               if Evaluation.query.filter_by(entite_id=e.id, statut="validee").count()]
    entite = Entite.query.get_or_404(entite_id) if entite_id else (entites[0] if entites else None)
    if not entite:
        return render_template("plan_action.html", entite=None, entites=entites, items=[])

    ref_cards = target_scores_summary(entite_id=entite.id)
    ref_id = request.args.get("ref_id", type=int)
    card = next((c for c in ref_cards if c["ref"].id == ref_id), None) if ref_id \
        else next((c for c in ref_cards if c["ref"].is_active), ref_cards[0] if ref_cards else None)
    if not card:
        return render_template("plan_action.html", entite=entite, entites=entites,
                               items=[], ref_cards=ref_cards, ref=None)

    ev = card["eval"]
    max_niveau = card["max"]
    items = []
    for s in ev.scores:
        if not (0 < s.niveau < max_niveau):
            continue
        cap = s.capacite
        cur = next((n for n in cap.niveaux if n.niveau == s.niveau), None)
        nxt = next((n for n in cap.niveaux if n.niveau == s.niveau + 1), None)
        items.append({
            "cap": cap, "dim": cap.dimension,
            "niveau": s.niveau, "cur_nom": cur.nom if cur else str(s.niveau),
            "next_nom": nxt.nom if nxt else "", "action": nxt.description if nxt else "",
            "prio": "Haute" if s.niveau <= max_niveau - 2 else "Moyenne",
        })
    items.sort(key=lambda x: (x["niveau"], x["dim"].numero))
    items = items[:8]

    return render_template("plan_action.html",
        entite=entite, entites=entites, items=items,
        ref_cards=ref_cards, ref=card["ref"], evaluation=ev, max_niveau=max_niveau)


@app.route("/exporter")
def exporter():
    """Exports & partage (L_EXPORT)."""
    campagnes = campagnes_with_results()
    return render_template("exporter.html", campagnes=campagnes)


# ──────────────────────────────────────────────
# Exports CSV
# ──────────────────────────────────────────────

def csv_response(rows, filename):
    out = io.StringIO()
    writer = csv.writer(out, delimiter=";")
    writer.writerows(rows)
    return Response(
        "\ufeff" + out.getvalue(),  # BOM pour Excel
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/export/campagne/<int:campagne_id>.csv")
def export_campagne_csv(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    validated = Evaluation.query.filter_by(campagne_id=campagne.id, statut="validee").all()
    rows = [["campagne", "cible", "referentiel", "dimension", "capacite", "nom_capacite",
             "portee", "niveau", "niveau_nom", "justification"]]
    for ev in validated:
        for s in ev.scores:
            cap = s.capacite
            niveau_nom = next((n.nom for n in cap.niveaux if n.niveau == s.niveau), "Non applicable")
            rows.append([campagne.label, ev.cible_nom, ev.referentiel.label,
                         cap.dimension.nom, cap.numero, cap.nom, cap.portee,
                         s.niveau if s.niveau > 0 else "NA", niveau_nom, s.justification or ""])
    return csv_response(rows, f"campagne-{campagne.id}-scores.csv")


@app.route("/export/entites.csv")
def export_entites_csv():
    rows = [["entite", "type", "direction", "referentiel", "score", "max", "pct", "date"]]
    for e in Entite.query.order_by(Entite.nom).all():
        for card in target_scores_summary(entite_id=e.id):
            rows.append([e.nom, e.type, e.direction or "", card["ref"].label,
                         card["score"], card["max"], card["pct"],
                         card["eval"].date_evaluation.strftime("%Y-%m-%d")])
    return csv_response(rows, "entites-scores.csv")


# ──────────────────────────────────────────────
# API JSON (conservées)
# ──────────────────────────────────────────────

@app.route("/api/evaluation/<int:evaluation_id>/scores")
def api_evaluation_scores(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    dim_scores = compute_scores_by_dimension(evaluation)
    return jsonify({
        "cible": evaluation.cible_nom,
        "referentiel": evaluation.referentiel.label,
        "score_global": global_score(evaluation),
        "dimensions": [
            {"nom": d["nom"], "numero": d["numero"], "moyenne": d["moyenne"]}
            for d in dim_scores.values()
        ],
    })


@app.route("/api/dashboard")
def api_dashboard():
    nb_entites = Entite.query.count()
    nb_sites = Site.query.count()
    nb_evaluations = Evaluation.query.filter_by(statut="validee").count()
    nb_referentiels = ReferentielVersion.query.count()
    nb_campagnes = Campagne.query.count()
    org_evals = Evaluation.query.filter(Evaluation.statut == "validee",
                                        Evaluation.entite_id.isnot(None)).all()
    moyennes = [global_score(ev) for ev in org_evals]
    score_moyen = round(sum(moyennes) / len(moyennes), 1) if moyennes else 0
    return jsonify([
        {"label": "Organisations", "valeur": nb_entites, "icone": "ri-building-line"},
        {"label": "Sites", "valeur": nb_sites, "icone": "ri-global-line"},
        {"label": "Référentiels", "valeur": nb_referentiels, "icone": "ri-book-open-line"},
        {"label": "Évaluations validées", "valeur": nb_evaluations, "icone": "ri-checkbox-circle-line"},
        {"label": "Campagnes", "valeur": nb_campagnes, "icone": "ri-calendar-line"},
        {"label": "Score moyen", "valeur": score_moyen, "icone": "ri-bar-chart-box-line"},
    ])


@app.route("/api/entites/scores")
def api_entites_scores():
    result = []
    for e in Entite.query.order_by(Entite.nom).all():
        cards = target_scores_summary(entite_id=e.id)
        result.append({
            "nom": e.nom, "type": e.type,
            "scores": [{"referentiel": c["ref"].label, "score": c["score"],
                        "max_niveau": c["max"], "pct": c["pct"]} for c in cards],
        })
    return jsonify(result)


@app.route("/api/sites/scores")
def api_sites_scores():
    result = []
    for s in Site.query.order_by(Site.nom).all():
        cards = target_scores_summary(site_id=s.id)
        result.append({
            "nom": s.nom, "organisation": s.organisation.nom,
            "scores": [{"referentiel": c["ref"].label, "score": c["score"],
                        "max_niveau": c["max"], "pct": c["pct"]} for c in cards],
        })
    return jsonify(result)


@app.route("/api/campagne/<int:campagne_id>/participation")
def api_campagne_participation(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    st = campagne_stats(campagne)
    return jsonify({
        "campagne": campagne.label, "statut": campagne.statut,
        "attendus": st["attendus"], "valides": st["valides"],
        "brouillons": st["brouillons"], "manquants": st["manquants"],
        "participation_pct": st["pct"],
    })


# ──────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
