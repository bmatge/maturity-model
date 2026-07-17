# Refonte UI — implémentation de la maquette « Maturité numérique.dc.html »

Source : projet Claude Design « Redesign app interface DSFR » (maquette 3 espaces par rôle,
fondée sur docs/redesign/01-brief, 02-personas, 03-taches).

## Décisions de périmètre (brief /goal du 2026-07-18)

- **DSFR natif d'abord** : composants natifs (header, sidemenu, btn, badge, table, accordion,
  tabs, modal, callout, alert, tile, segmented, toggle, upload…) partout où possible ;
  CSS custom minimal (`custom.css`) uniquement pour ce que DSFR n'a pas : level-picker,
  heatmap, exec-cards, barre de progression, print.
- **Charts** : lib `dsfr-data` (CDN dsfr-data@0 + dsfr-chart@2.1.1 + chart.js) —
  `<dsfr-data-source data='[...]'>` inline + `<dsfr-data-chart type="radar|line|bar|gauge">`.
- **Comptes utilisateurs (pré-Authentik)** : table `user` (nom, email, rôle, périmètre).
  3 rôles à compte : `repondant`, `pilote`, `admin` — droit `global` / `entite` / `site`
  (scope_type + scope_id). + rôle `lecteur` public (sans compte). Le header propose un
  sélecteur « se connecter en tant que » (session) — remplacé plus tard par Authentik.
  Page « Utilisateurs & rôles » réelle (CRUD).
- **Portées C/D/P** : légende unifiée = Centrale (SIRCOM) / Distribuée (bureaux) / Partagée
  (coordination), conformément à la maquette. Corrige l'incohérence Cabinet/Direction/Publique.
- **Score global unifié** : moyenne des moyennes de dimension, partout (résultats inclus).
- **Non applicable** : Score.niveau = 0 (pas de migration), exclu de toutes les moyennes.
- **Campagne ↔ référentiel** : colonne `referentiel_id` (nullable) réintroduite sur campagne
  pour la comparabilité + le pré-remplissage des invitations.
- **Invitations** : liens pré-remplis (triplet) + mailto ; pas d'envoi serveur.
- **Import référentiel** : JSON implémenté ; xlsx annoncé comme « à venir » sur la page.
- **Export** : CSV réels (scores campagne, scores entités) ; « PDF » = feuille de style print.
- **Charts** : DSFR Chart (radar/line) conservé — cohérence écosystème dsfr-data.

## Phase 0 — Fondations
- [ ] `webapp/static/ui.css` : tokens DSFR v1.14 (colors_and_type.css adapté, fonts Marianne
      via CDN @gouvfr/dsfr) + classes composants extraites de la maquette (btn, card, chip,
      table, sidebar, kpi, progress, level-picker, tabs, modal, alert…)
- [ ] `webapp/static/bloc-marque.svg` (récupéré du projet design)
- [ ] `webapp/static/app.js` : interactions (accordéons, modale suppression, tabs, filtre
      portée, recherche capacité, justification toggle, NA toggle, print)

## Phase 1 — Backend (contrat de données)
- [ ] models.py : `CampagneParticipant` (campagne_id, entite_id, evaluateur) ;
      `Campagne.referentiel_id` nullable
- [ ] migrate_db() : ADD COLUMN campagne.referentiel_id ; CREATE TABLE campagne_participant
- [ ] Helpers : exclure niveau=0 (NA) des moyennes ; `global_score()` = moyenne des moyennes
- [ ] Rôles : session['role'], route `/role/<r>`, `/` redirige selon rôle
- [ ] Répondant : `/mes-evaluations` (r_home) ; `/evaluation/<id>/recap` (r_recap) ;
      fill : support NA + ancres dimensions
- [ ] Pilote : `/campagne/<id>` (détail à onglets suivi/périmètre/invitations/réglages) ;
      campagne edit/clôture/réouverture ; entité edit ; site edit ;
      `/referentiels` (liste + activer/désactiver) ; `/referentiels/import` (JSON)
- [ ] Lecteur : `/restitution` (l_home exécutif) ; `/restitution/organisation/<id>` (l_entity) ;
      `/comparer` (l_compare) ; `/plan-action/<id>` (l_action) ; `/exporter` (l_export)
- [ ] Exports CSV : `/export/campagne/<id>.csv`, `/export/entites.csv`

## Phase 2 — Templates (maquette = source de vérité visuelle)
- [ ] base.html : header (bloc-marque + switcher rôle) + sidebar par rôle + carte contextuelle
- [ ] Espace répondant : mes_evaluations, evaluation_new, evaluation_fill (2 colonnes,
      sticky progression), evaluation_recap, evaluation_results (2 vitesses + vue experte)
- [ ] Référentiel partagé : referentiel.html (échelle pédagogique, filtres portée, accordéons)
- [ ] Espace pilote : index (tdb), campagnes, campagne_form, campagne_detail (4 onglets),
      campagne_dashboard (radar + stats + heatmap), entites, entite_form, sites, site_form,
      referentiels, referentiel_import
- [ ] Espace lecteur : restitution, restitution_entite, entite_evolution (reskin),
      comparer, plan_action, exporter
- [ ] Modale de confirmation suppression (partagée)

## Phase 3 — Vérification
- [ ] Lancer l'app (docker ou flask), parcourir les 3 espaces au navigateur
- [ ] Parcours critique : créer campagne → périmètre → invitation → remplir → valider →
      restitution → export
- [ ] Migrations sur DB existante (seed) sans casse

## Review

(à compléter en fin de tâche)
