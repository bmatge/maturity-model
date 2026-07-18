"""Jeu de données de démonstration — régénérable et déterministe.

Détruit tout le contenu métier (campagnes, évaluations, scores, participants,
organisations, sites, utilisateurs) puis recrée un scénario cohérent :

- 6 organisations + 6 sites rattachés, avec leurs répondants (faux comptes) ;
- 4 campagnes semestrielles Design-org-v1 (S1 2025 → S2 2026, la dernière en
  cours avec brouillons et retardataire — pour la démo du suivi/relances) ;
- 1 campagne ComNum 2026 (multi-référentiel sur 3 organisations) + une
  évaluation ComNum antérieure hors campagne (évolution multi-ref) ;
- 3 vagues d'évaluations Design-site-v1 pour chaque site (évolution) ;
- justifications réalistes (~2 réponses sur 3), quelques non-applicables.

L'histoire racontée : la maturité progresse semestre après semestre, la
dimension « Évaluation & amélioration continue » reste le chantier transverse,
le Bureau com — Jeunesse décroche en 2026.

Usage :
    python demo_seed.py            # local (DATABASE_PATH respecté)
    docker compose exec web python demo_seed.py   # sur le VPS
"""

import random
from datetime import datetime, date, timedelta

from app import app
from models import (db, ReferentielVersion, Dimension, Entite, Site, Campagne,
                    CampagneParticipant, Evaluation, Score, User)

random.seed(20260718)

# ── Patrimoine ─────────────────────────────────────────────────────

ORGS = [
    # nom, type, direction, base de maturité (0..1), répondant
    ("SIRCOM", "SIRCOM", "Secrétariat général", 0.56, "Marc Roux"),
    ("Bureau com — Santé", "Bureau", "DGS", 0.50, "Camille Durand"),
    ("Bureau com — Travail", "Bureau", "DGT", 0.62, "Karim Nguyen"),
    ("Bureau com — Économie", "Bureau", "DGE", 0.45, "Sophie Petit"),
    ("Bureau com — Jeunesse", "Bureau", "DJEPVA", 0.42, "Jeanne Blanc"),
    ("Délégation numérique", "Bureau", "Secrétariat général", 0.70, "Lise Fabre"),
]

SITES = [
    # nom, url, organisation, base de maturité
    ("economie.gouv.fr", "https://www.economie.gouv.fr", "SIRCOM", 0.62),
    ("sante.gouv.fr", "https://sante.gouv.fr", "Bureau com — Santé", 0.52),
    ("travail-emploi.gouv.fr", "https://travail-emploi.gouv.fr", "Bureau com — Travail", 0.60),
    ("code.travail.gouv.fr", "https://code.travail.gouv.fr", "Bureau com — Travail", 0.72),
    ("jeunes.gouv.fr", "https://jeunes.gouv.fr", "Bureau com — Jeunesse", 0.44),
    ("Alizé (intranet)", "", "Bureau com — Économie", 0.38),
]

# Biais par numéro de dimension : l'« évaluation continue » (dim 3 du Design)
# est faible partout, la conception est plutôt forte — cf. l'histoire.
DIM_BIAS = {1: -0.04, 2: +0.10, 3: -0.13, 4: 0.0, 5: -0.02, 6: +0.03, 7: -0.06}

JUSTIFS = {
    1: ["Rien de formalisé à ce jour, tout repose sur les personnes.",
        "Pratique inexistante faute de temps et de moyens dédiés.",
        "Jamais mis en place ; identifié comme un manque lors du dernier séminaire."],
    2: ["Pratique réelle mais dépendante de quelques personnes clés.",
        "Mis en œuvre sur les gros projets uniquement, sans outillage partagé.",
        "Démarche engagée cette année, encore irrégulière.",
        "Un premier guide existe, application inégale selon les projets."],
    3: ["Pratique outillée, documentée et suivie dans la durée.",
        "Systématisé depuis la refonte : chaque projet passe par cette étape.",
        "Ancré dans nos rituels d'équipe, revue à chaque sprint.",
        "Process partagé avec les directions métiers, indicateurs suivis."],
    4: ["Pratique pérenne, intégrée aux processus ministériels et auditée.",
        "Amélioration continue en place, revue annuelle documentée."],
}


def niveau_for(v, max_niveau):
    """Valeur continue 0..1 → niveau 1..max (seuils réalistes)."""
    if max_niveau == 3:
        return 1 + (v > 0.38) + (v > 0.70)
    return 1 + (v > 0.30) + (v > 0.55) + (v > 0.80)


def fill_eval(ev, ref, base, na_caps=(), justif_ratio=0.66):
    """Remplit tous les scores d'une évaluation selon la maturité de base."""
    from app import get_max_niveau
    max_niv = get_max_niveau(ref)
    for dim in Dimension.query.filter_by(referentiel_id=ref.id).all():
        for cap in dim.capacites:
            if cap.numero in na_caps:
                db.session.add(Score(evaluation_id=ev.id, capacite_id=cap.id, niveau=0,
                                     justification="Sans objet pour ce périmètre."))
                continue
            v = base + DIM_BIAS.get(dim.numero, 0) + random.uniform(-0.13, 0.13)
            niv = max(1, min(max_niv, niveau_for(v, max_niv)))
            justif = random.choice(JUSTIFS[min(niv, 4)]) if random.random() < justif_ratio else ""
            db.session.add(Score(evaluation_id=ev.id, capacite_id=cap.id,
                                 niveau=niv, justification=justif))


def make_eval(ref, campagne, entite=None, site=None, evaluateur="", base=0.5,
              dt=None, statut="validee", na_caps=(), partial=None):
    ev = Evaluation(referentiel_id=ref.id,
                    campagne_id=campagne.id if campagne else None,
                    entite_id=entite.id if entite else None,
                    site_id=site.id if site else None,
                    evaluateur=evaluateur, statut=statut,
                    date_evaluation=dt or datetime.utcnow())
    db.session.add(ev)
    db.session.flush()
    if partial is None:
        fill_eval(ev, ref, base, na_caps=na_caps)
    else:
        # brouillon partiel : ne remplir que les N premières capacités
        from app import get_max_niveau
        max_niv = get_max_niveau(ref)
        caps = [c for d in Dimension.query.filter_by(referentiel_id=ref.id)
                .order_by(Dimension.numero) for c in d.capacites][:partial]
        for cap in caps:
            v = base + random.uniform(-0.13, 0.13)
            db.session.add(Score(evaluation_id=ev.id, capacite_id=cap.id,
                                 niveau=max(1, min(max_niv, niveau_for(v, max_niv)))))
    return ev


def run():
    with app.app_context():
        # S'assurer que le schéma et les référentiels sont en place
        from app import migrate_db
        db.create_all()
        migrate_db()
        from seed import seed_referentiel, seed_mini_referentiels
        seed_referentiel()
        seed_mini_referentiels()

        # ── Table rase du contenu métier ──
        for model in (Score, Evaluation, CampagneParticipant, Campagne, Site, Entite, User):
            model.query.delete()
        db.session.commit()
        print("contenu métier purgé")

        design_org = ReferentielVersion.query.filter_by(label="Design-org-v1").first()
        design_site = ReferentielVersion.query.filter_by(label="Design-site-v1").first()
        comnum = ReferentielVersion.query.filter_by(label="v2.0").first()
        design_org.is_active = True
        design_site.is_active = True

        # ── Organisations, sites, comptes ──
        orgs, users = {}, {}
        for nom, typ, direction, base, resp in ORGS:
            e = Entite(nom=nom, type=typ, direction=direction,
                       description=f"{typ} — {direction}. Répondant : {resp}.")
            db.session.add(e)
            db.session.flush()
            orgs[nom] = (e, base, resp)
            local = resp.lower().replace(" ", ".").replace("é", "e").replace("è", "e")
            e.email_contact = f"{local}@finances.gouv.fr"
            users[nom] = User(nom=resp, email=f"{local}@finances.gouv.fr",
                              role="repondant", scope_type="entite", scope_entite_id=e.id)
            db.session.add(users[nom])
        db.session.add(User(nom="Nadia Bensaïd", email="nadia.bensaid@finances.gouv.fr",
                            role="pilote", scope_type="global"))
        db.session.add(User(nom="Admin technique", email="admin.maturite@finances.gouv.fr",
                            role="admin", scope_type="global"))

        sites = {}
        for nom, url, org_nom, base in SITES:
            s = Site(nom=nom, url=url, organisation_id=orgs[org_nom][0].id,
                     description=f"Site rattaché à {org_nom}.")
            db.session.add(s)
            db.session.flush()
            sites[nom] = (s, base, orgs[org_nom][2])
        db.session.commit()
        print(f"{len(orgs)} organisations, {len(sites)} sites, {len(orgs) + 2} comptes")

        # ── Campagnes semestrielles Design-org ──
        camps = [
            ("Campagne S1 2025 — Design", date(2025, 1, 15), date(2025, 6, 30), "terminee"),
            ("Campagne S2 2025 — Design", date(2025, 7, 15), date(2025, 12, 31), "terminee"),
            ("Campagne S1 2026 — Design", date(2026, 1, 15), date(2026, 6, 30), "terminee"),
            ("Campagne S2 2026 — Design", date(2026, 7, 1), date(2026, 12, 31), "en_cours"),
        ]
        campagnes = []
        for label, deb, fin, statut in camps:
            c = Campagne(label=label, date_debut=deb, date_fin=fin,
                         statut=statut, referentiel_id=design_org.id)
            db.session.add(c)
            db.session.flush()
            campagnes.append(c)

        # progression par vague ; le Bureau Jeunesse décroche en 2026
        WAVE_GAIN = [0.0, 0.07, 0.13, 0.18]
        JEUNESSE_GAIN = [0.0, 0.05, 0.05, 0.04]
        validation_dates = [date(2025, 6, 10), date(2025, 12, 8), date(2026, 6, 9), date(2026, 7, 8)]

        for wave, camp in enumerate(campagnes):
            for i, (nom, (e, base, resp)) in enumerate(orgs.items()):
                # S1 2025 : la Jeunesse n'avait pas participé (l'adoption progresse)
                in_perimeter = not (wave == 0 and nom == "Bureau com — Jeunesse")
                if in_perimeter:
                    db.session.add(CampagneParticipant(campagne_id=camp.id, entite_id=e.id,
                                                       evaluateur=resp))
                if not in_perimeter:
                    continue
                gain = (JEUNESSE_GAIN if nom == "Bureau com — Jeunesse" else WAVE_GAIN)[wave]
                dt = datetime.combine(validation_dates[wave] + timedelta(days=i), datetime.min.time()) \
                    .replace(hour=9 + i)
                if wave < 3:
                    make_eval(design_org, camp, entite=e, evaluateur=resp,
                              base=base + gain, dt=dt,
                              na_caps=("1.4",) if nom == "Bureau com — Économie" and wave == 0 else ())
                else:
                    # campagne en cours : 3 validées, 2 brouillons, 1 non commencée
                    if nom in ("SIRCOM", "Délégation numérique", "Bureau com — Travail"):
                        make_eval(design_org, camp, entite=e, evaluateur=resp,
                                  base=base + gain, dt=dt)
                    elif nom == "Bureau com — Santé":
                        make_eval(design_org, camp, entite=e, evaluateur=resp,
                                  base=base + gain, dt=datetime.utcnow(), statut="brouillon", partial=9)
                    elif nom == "Bureau com — Économie":
                        make_eval(design_org, camp, entite=e, evaluateur=resp,
                                  base=base + gain, dt=datetime.utcnow(), statut="brouillon", partial=4)
                    # Jeunesse : non commencée (retardataire à relancer)
        db.session.commit()
        print("4 campagnes Design-org (3 terminées + 1 en cours)")

        # ── Campagne ComNum (multi-référentiel) + antériorité hors campagne ──
        c_comnum = Campagne(label="Campagne ComNum 2026", date_debut=date(2026, 2, 1),
                            date_fin=date(2026, 3, 31), statut="terminee",
                            referentiel_id=comnum.id)
        db.session.add(c_comnum)
        db.session.flush()
        for j, nom in enumerate(("SIRCOM", "Bureau com — Santé", "Délégation numérique")):
            e, base, resp = orgs[nom]
            db.session.add(CampagneParticipant(campagne_id=c_comnum.id, entite_id=e.id, evaluateur=resp))
            make_eval(comnum, c_comnum, entite=e, evaluateur=resp, base=base + 0.06,
                      dt=datetime(2026, 3, 10 + j, 10))
        e, base, resp = orgs["SIRCOM"]
        make_eval(comnum, None, entite=e, evaluateur=resp, base=base - 0.06,
                  dt=datetime(2025, 3, 12, 10))
        db.session.commit()
        print("campagne ComNum 2026 (3 orgs) + 1 évaluation ComNum 2025 hors campagne")

        # ── 3 vagues d'évaluations de sites (Design-site) ──
        site_waves = [datetime(2025, 6, 16, 14), datetime(2025, 12, 10, 14), datetime(2026, 6, 15, 14)]
        for w, wdate in enumerate(site_waves):
            for k, (nom, (s, base, resp)) in enumerate(sites.items()):
                na = ("2.4", "2.5") if "intranet" in nom.lower() else ()
                make_eval(design_site, None, site=s, evaluateur=resp,
                          base=base + 0.06 * w, dt=wdate + timedelta(days=k),
                          na_caps=na)
        db.session.commit()
        print(f"{len(sites)} sites × 3 vagues Design-site")

        nb = {m.__name__: m.query.count() for m in (Entite, Site, Campagne, Evaluation, Score, User)}
        print("état final :", nb)


if __name__ == "__main__":
    run()
