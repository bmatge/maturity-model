# 04 — Implémentation de la maquette (2026-07-18)

Maquette source : projet Claude Design « Redesign app interface DSFR »
(`Maturité numérique.dc.html`), elle-même fondée sur 01-brief, 02-personas, 03-taches.
Implémentée en DSFR 1.14 natif + dsfr-data (charts), commits `43c3550` → `6d7ea62`.

## Correspondance maquette → application

| Écran maquette | Route | État |
|---|---|---|
| R_HOME Mes évaluations | `/mes-evaluations` | ✅ brouillons / invitations / validées, scope par droit |
| R_START Démarrer | `/evaluation/new` | ✅ triplet guidé, anti-doublon réel (redirection vers l'existante) |
| R_FILL Questionnaire | `/evaluation/<id>/fill` | ✅ 2 colonnes, progression sticky, NA (niveau 0), justifications |
| R_RECAP Vérifier | `/evaluation/<id>/recap` | ✅ complétude, capacités manquantes, aperçu profil |
| R_RESULTS Résultats | `/evaluation/<id>/results` | ✅ 2 vitesses : score hero + « 3 choses à retenir » + delta ; vue experte (radar, détail) |
| REF_VIEW Référentiel | `/referentiel` | ✅ échelle pédagogique, recherche, filtres portée C/D/P **unifiés** (Centrale/Distribuée/Partagée) |
| P_HOME Tableau de bord | `/` (rôle pilote) | ✅ 6 KPIs, campagne en cours, radar moyen, classement |
| P_CAMPAIGNS | `/campagnes` | ✅ avancement par périmètre |
| P_CAMPAIGN_NEW | `/campagnes/new` | ✅ avec référentiel de campagne (comparabilité) |
| P_CAMPAIGN_DETAIL | `/campagne/<id>` | ✅ fr-tabs : Suivi / Périmètre / Invitations (lien pré-rempli + copie) / Réglages (clôture ↔ réouverture, zone danger) |
| P_DASHBOARD Restitution campagne | `/campagne/<id>/dashboard` | ✅ radar multi-séries, stats ± écart-type, heatmap 3/4 niveaux + NA, print + CSV |
| P_ENTITIES / P_ENTITY_FORM | `/entites`, `/entites/<id>/edit` | ✅ édition ajoutée (créer/modifier/supprimer) |
| P_SITES / P_SITE_FORM | `/sites`, `/sites/<id>/edit` | ✅ idem |
| P_REFERENTIELS | `/referentiels` | ✅ activation fr-toggle ; « famille » non implémentée (pas en base) |
| P_REF_IMPORT | `/referentiels/import` | ✅ JSON structuré ; xlsx à venir |
| P_USERS | `/utilisateurs` | ✅ CRUD comptes — 3 rôles (répondant/pilote/admin) × droits (global/entité/site) + lecteur public sans compte |
| L_HOME Vue d'ensemble | `/restitution` | ✅ 3 messages exécutifs (progression vs campagne précédente, chantier transverse, entité qui décroche) + fiabilité de la donnée |
| L_ENTITY Fiche organisation | `/restitution/organisation/<id>` | ✅ multi-référentiels + radar + sites rattachés |
| L_EVOLUTION | `/evolution` | ✅ line chart par dimension, par référentiel |
| L_COMPARE | `/comparer` | ✅ 2 organisations **ou** 2 campagnes, radar + écarts |
| L_ACTION Plan d'action | `/plan-action/<id>` | ✅ dérivé du critère du niveau supérieur, priorités |
| L_EXPORT | `/exporter` | ✅ print PDF, CSV campagne + organisations, lien de partage |
| Modale suppression | partagée (`base.html` + `app.js`) | ✅ tous les deletes passent par elle |

## Décisions prises pendant l'implémentation

- **Incohérences maquette corrigées** : icônes ri-* → fr-icon-*, composants custom de la
  maquette remplacés par les natifs DSFR (header, sidemenu, tabs, accordéons, badges,
  toggle, upload, alerts, callouts, tables 1.14) ; custom.css réduit à ce que DSFR n'a
  pas (level-picker, heatmap, barres de progression, exec-cards, print).
- **Score global unifié** : moyenne des moyennes de dimension partout (résolution de la
  contradiction historique).
- **Légende C/D/P unifiée** : Centrale (SIRCOM) / Distribuée (bureaux) / Partagée.
- **NA** : `Score.niveau = 0`, exclu de toutes les moyennes.
- **Charts** : dsfr-data (`<dsfr-data-source data='…'>` inline + `<dsfr-data-chart>`
  radar/line/bar), radar multi-séries via `series-field`.
- **Comptes pré-Authentik** : sélecteur d'identité dans le header (session). Les guards
  sont « soft » (tout le monde peut changer d'identité) — l'enforcement réel viendra
  avec Authentik.

## Vérifié (2026-07-18, HTTP de bout en bout sur DB seed migrée + scénario démo)

- Camille : brouillon 9/15 avec NA → complétion → récap 15/15 → validation → résultats
  (delta vs 2025, 3 choses à retenir, NA affiché) ; scope entité respecté.
- Nadia : création campagne → périmètre → invitation (auto-création de l'évaluation,
  ComNum 4 niveaux OK) → suivi/relances → clôture → réouverture éval → dashboard
  (45 cellules heatmap) → import JSON + activation → CRUD utilisateurs → suppression.
- Marc (public) : restitution (+20 pts vs 2025, participation 60 %, justifiées 78 %),
  évolution, comparaison (orgs + campagnes), plan d'action, exports CSV ; guard des
  pages pilote OK.
- Migrations : DB seed du repo (ancien schéma) migrée sans casse.

## Reste à faire → issues GitHub

Voir les issues ouvertes du repo (relance groupée, import xlsx, Authentik,
consolidation sites → organisation, rapport PDF serveur, QA visuelle navigateur).
