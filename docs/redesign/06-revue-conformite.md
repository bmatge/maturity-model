# 06 — Revue de conformité DSFR / dsfr-data & appropriation par profils (2026-07-18)

> **État : corrigé le 2026-07-18** — lots 1 et 2 appliqués intégralement, lot 3 appliqué
> sauf deux chantiers tracés en issues (mode « une dimension à la fois » ; `y-min/y-max`
> radar dans la lib dsfr-data upstream). Voir le commit de correction.

Trois audits croisés (conformité DSFR 1.14 vérifiée contre le CSS réel du CDN,
conformité dsfr-data vérifiée contre la spec officielle, audit UX par personas —
rapport détaillé : `05-audit-ux.md`) + contrôle visuel navigateur.

Constat général : le socle est sain (anatomies fr-table/fr-tabs/fr-modal/fr-accordion
conformes, versions CDN exactes, états vides traités, progressive disclosure réelle).
Les findings ci-dessous sont classés en trois lots actionnables.

---

## LOT 1 — Corrections objectives (conformité, a11y, bugs de confiance)

### Critiques
| # | Sujet | Détail |
|---|---|---|
| 1.1 | **Promesse de sauvegarde mensongère** | Le questionnaire n'a AUCUN autosave alors que le lien de sortie dit « Quitter (le brouillon est conservé) ». Une répondante qui quitte sans « Sauvegarder » perd tout. Fix minimal : « Quitter » = submit qui sauvegarde + garde `beforeunload` si modifications non enregistrées. |
| 1.2 | **Guard manquant sur la création d'évaluation** | `/evaluation/new` et `/invitation/...` accessibles au lecteur public (vu au spot-check) : n'importe quel membre du lab sans groupe maturity peut créer des évaluations. Guard `repondant+` requis. |
| 1.3 | **RGAA légal** : pas de `fr-skiplinks`, footer sans bloc `fr-footer__bottom` (mention « Accessibilité : non conforme », mentions légales) — obligation légale. |
| 1.4 | **A11y du cœur fonctionnel** : `.level-option` sans `aria-pressed` (un lecteur d'écran ne sait pas quel niveau est choisi) ; textarea justification sans label. |

### Majeurs (mécaniques)
- Classes inexistantes en 1.14.4 : `fr-icon-file-copy-line` → `fr-icon-clipboard-line` ; `fr-icon-focus-line` → `fr-icon-focus-3-line` ; `fr-col-auto`/`fr-col-md-auto` (n'existent pas — rendu par accident) ; `fr-sidemenu__item--active` (morte).
- 12 `fr-card` sans anatomie complète (même famille que le bug plan d'action) → remplacer par `.panel`.
- `fr-btns-group` sans `ul > li` (8 templates) ; tables sans `caption` (5) + heatmap rapport sans `scope` ; titres de sections en `<p class="panel__title">` → `<h2>/<h3>` (le rapport COPIL n'a aucun h2).
- **Charts muets pour les lecteurs d'écran** : aucun `dsfr-data-a11y` (description + tableau alternatif + CSV) sur les 7 pages à charts — prioritaire sur les restitutions.
- Courbes d'évolution : `y-min="0" y-max="N"` natifs de dsfr-data (la rustine JS ne doit rester que pour les radars, non couverts par la spec).
- Auto-submit `onchange` des selects de filtres (10 occurrences) : changement de contexte non annoncé + pénible au clavier → bouton « Appliquer » ou liens.
- Bouton « Rechercher » de la barre de recherche du référentiel inopérant.

### Mineurs (finitions)
Tokens texte utilisés en background (`--background-flat-*` existent), `--text-inverted-blue-france` sur les onglets d'espace, `white-space: normal` global → `fr-cell--multiline`, badge identité (fr-badge détourné), `fr-badge--new` pour admin, flèches « → » unicode → icônes DSFR, incohérences (tailles de h1, `fr-link--sm`, badges avec/sans icône, wording des exports), feedback « Copié ✓ » silencieux pour les SR (3 implémentations à factoriser + `aria-live`), boutons `disabled` avec `title` inaccessible → `fr-hint-text`, alerte recap en h3 après h1, jauges décoratives sans `aria-hidden`.

## LOT 2 — Wording & appropriation (chargés de com non techniciens)

Priorité Camille (détail avant→après dans `05-audit-ux.md`) :
- **« Vérifiez le triplet avant de commencer »** → « Vérifiez le référentiel, la cible et la campagne avant de commencer. »
- **« v2.0 »** comme label de référentiel (affiché en titre de résultats « v2.0 — SIRCOM ») → renommer « ComNum v2.0 » dans le seed.
- **Portée C/D/P** : sens uniquement au survol (invisible tactile/clavier) → légende visible sur le questionnaire ou masquer côté répondant.
- « entité » vs « organisation » pour le même concept → tout en « organisation ».
- « Votre nom (évaluateur) » → « Votre nom » + hint « Il apparaîtra comme auteur de l'évaluation ».
- « Heatmap » → « Carte thermique » (ou sous-titre explicatif).
- Sauvegarde du brouillon qui recharge la page en haut → conserver l'ancre de la dimension courante.
- « À renforcer : Écosystème éditorial (2.14/4) » → arrondir à 1 décimale.

## LOT 3 — Refactos à arbitrer (améliorations structurantes)

1. **Autosave AJAX** du questionnaire (sauvegarde à chaque réponse) — le vrai fix du 1.1 ; à tracer en ADR.
2. **Mode « une dimension à la fois »** (stepper) pour les longs référentiels (ComNum = 44 capacités) — anti-fatigue Camille.
3. **Écran « Démarrer » réservé aux cas hors campagne** : le chemin normal de Camille est l'invitation pré-remplie ; simplifier ou masquer le formulaire triplet pour les répondants.
4. **DataBox dsfr-data sur le rapport COPIL** (titre, source, date, switch tableau, CSV intégré) — extrait prêt dans l'audit dsfr-data.
5. **`y-min`/`y-max` pour le type radar dans la lib dsfr-data elle-même** (upstream bmatge/dsfr-data) → suppression complète de la rustine `data-scale-max`.
6. **Plafond de séries** sur le radar comparatif (top N + moyenne) au-delà de ~5 entités.
7. Palette `default` (Bleu France) explicite sur les radars mono-série.

---

Décomptes : DSFR 4 bloquants / 10 majeurs / 18 mineurs · dsfr-data 2 majeurs / 2 mineurs / 3 suggestions · UX 1 critique / ~10 quick wins / 3 refactos.
