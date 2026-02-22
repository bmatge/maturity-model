"""
Modèle de données pour le suivi de maturité de la communication numérique.

Axes de variabilité :
- Le référentiel évolue (versions)
- Les entités sont multiples (SIRCOM + bureaux)
- Les évaluations se répètent dans le temps (campagnes)
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ──────────────────────────────────────────────
# Référentiel (versionné)
# ──────────────────────────────────────────────

class ReferentielVersion(db.Model):
    """Une version du référentiel de maturité (ex: v2.0, v2.1)."""
    __tablename__ = "referentiel_version"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), nullable=False, unique=True)  # "v2.0"
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)

    dimensions = db.relationship("Dimension", back_populates="referentiel",
                                 cascade="all, delete-orphan",
                                 order_by="Dimension.numero")

    def __repr__(self):
        return f"<Referentiel {self.label}>"


class Dimension(db.Model):
    """Une dimension du référentiel (ex: Vision & positionnement)."""
    __tablename__ = "dimension"

    id = db.Column(db.Integer, primary_key=True)
    referentiel_id = db.Column(db.Integer, db.ForeignKey("referentiel_version.id"), nullable=False)
    numero = db.Column(db.Integer, nullable=False)  # 1..7
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    referentiel = db.relationship("ReferentielVersion", back_populates="dimensions")
    capacites = db.relationship("Capacite", back_populates="dimension",
                                cascade="all, delete-orphan",
                                order_by="Capacite.numero")

    def __repr__(self):
        return f"<Dimension {self.numero}. {self.nom}>"


class Capacite(db.Model):
    """Une capacité évaluable (ex: 1.1 Vision stratégique)."""
    __tablename__ = "capacite"

    id = db.Column(db.Integer, primary_key=True)
    dimension_id = db.Column(db.Integer, db.ForeignKey("dimension.id"), nullable=False)
    numero = db.Column(db.String(10), nullable=False)  # "1.1", "7.9"
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    portee = db.Column(db.String(1), nullable=False)  # C, D, P

    dimension = db.relationship("Dimension", back_populates="capacites")
    niveaux = db.relationship("NiveauCritere", back_populates="capacite",
                              cascade="all, delete-orphan",
                              order_by="NiveauCritere.niveau")
    scores = db.relationship("Score", back_populates="capacite")

    def __repr__(self):
        return f"<Capacite {self.numero} {self.nom}>"


class NiveauCritere(db.Model):
    """Description d'un niveau de maturité pour une capacité donnée."""
    __tablename__ = "niveau_critere"

    id = db.Column(db.Integer, primary_key=True)
    capacite_id = db.Column(db.Integer, db.ForeignKey("capacite.id"), nullable=False)
    niveau = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4
    nom = db.Column(db.String(20), nullable=False)  # Émergent, Structuré, Intégré, Pérenne
    description = db.Column(db.Text, nullable=False)
    signaux_observables = db.Column(db.Text)

    capacite = db.relationship("Capacite", back_populates="niveaux")

    def __repr__(self):
        return f"<Niveau {self.niveau} pour {self.capacite.numero}>"


# ──────────────────────────────────────────────
# Entités évaluées
# ──────────────────────────────────────────────

class Entite(db.Model):
    """Une entité évaluable (SIRCOM ou bureau de communication)."""
    __tablename__ = "entite"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # "SIRCOM" ou "Bureau"
    direction = db.Column(db.String(200))  # direction de rattachement
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    evaluations = db.relationship("Evaluation", back_populates="entite",
                                  order_by="Evaluation.date_evaluation.desc()")

    def __repr__(self):
        return f"<Entite {self.nom}>"


# ──────────────────────────────────────────────
# Campagnes et évaluations
# ──────────────────────────────────────────────

class Campagne(db.Model):
    """Une campagne d'évaluation (ex: T1 2026, Audit annuel 2026)."""
    __tablename__ = "campagne"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    referentiel_id = db.Column(db.Integer, db.ForeignKey("referentiel_version.id"), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date)
    statut = db.Column(db.String(20), default="en_cours")  # en_cours, terminee

    referentiel = db.relationship("ReferentielVersion")
    evaluations = db.relationship("Evaluation", back_populates="campagne",
                                  cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campagne {self.label}>"


class Evaluation(db.Model):
    """Une évaluation = une entité évaluée lors d'une campagne."""
    __tablename__ = "evaluation"

    id = db.Column(db.Integer, primary_key=True)
    campagne_id = db.Column(db.Integer, db.ForeignKey("campagne.id"), nullable=False)
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"), nullable=False)
    evaluateur = db.Column(db.String(200))
    date_evaluation = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default="brouillon")  # brouillon, validee
    commentaire_global = db.Column(db.Text)

    campagne = db.relationship("Campagne", back_populates="evaluations")
    entite = db.relationship("Entite", back_populates="evaluations")
    scores = db.relationship("Score", back_populates="evaluation",
                             cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("campagne_id", "entite_id", name="uq_campagne_entite"),
    )

    def __repr__(self):
        return f"<Evaluation {self.entite.nom} — {self.campagne.label}>"


class Score(db.Model):
    """Un score attribué à une capacité dans une évaluation."""
    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey("evaluation.id"), nullable=False)
    capacite_id = db.Column(db.Integer, db.ForeignKey("capacite.id"), nullable=False)
    niveau = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4
    justification = db.Column(db.Text)  # pourquoi ce niveau
    signaux_constates = db.Column(db.Text)  # éléments observés

    evaluation = db.relationship("Evaluation", back_populates="scores")
    capacite = db.relationship("Capacite", back_populates="scores")

    __table_args__ = (
        db.UniqueConstraint("evaluation_id", "capacite_id", name="uq_eval_capacite"),
        db.CheckConstraint("niveau BETWEEN 1 AND 4", name="ck_score_niveau"),
    )

    def __repr__(self):
        return f"<Score {self.capacite.numero}={self.niveau}>"
