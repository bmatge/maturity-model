# Epic : Évaluation multi-référentiel (organisations + sites)

## Contexte

L'application permet aujourd'hui d'évaluer des **organisations** (SIRCOM, bureaux de communication) sur un référentiel unique de maturité de la communication numérique (7 dimensions, 44 capacités, 4 niveaux).

Le besoin évolue : il faut pouvoir évaluer aussi des **sites web** sur d'autres référentiels (accessibilité, éco-conception, qualité, design...), et faire le lien entre les sites et les organisations auxquelles ils appartiennent.

## Vision cible

```
Organisation (Entite)
    ├── évaluée sur N référentiels "organisation"
    │     ex: Maturité ComNum, Maturité Data, Accessibilité (volet orga)
    │
    └── possède N Sites
          └── évalués sur M référentiels "site"
                ex: Accessibilité (volet site), Éco-conception, Design
```

À terme, les scores des sites pourront contribuer implicitement à qualifier la maturité de l'organisation (ex: bons scores accessibilité des sites → maturité organisationnelle sur l'accessibilité). Ce lien n'est pas modélisé dans un premier temps.

## Décisions prises

| Décision | Choix | Justification |
|----------|-------|---------------|
| Modèle sites | Modèle `Site` séparé (pas de généralisation d'Entite) | Plus propre, attributs différents (URL, etc.) |
| Campagne | Une campagne = un seul type de cible | Simplicité des vues et de la logique |
| Référentiels | N référentiels possibles, chacun typé org ou site | Extensibilité maximale |
| Vues | Séparées organisations / sites dans un premier temps | Évolutif vers une vue consolidée plus tard |
| Niveaux | Nombre de niveaux flexible par référentiel (3, 4, ou autre) | Le réf. Design MEF utilise 3 niveaux, le ComNum 4 — pas de raison de forcer |
| Métadonnées sites | Seuls les critères scorables dans maturity-model | Les fiches descriptives (identité, socle technique…) seront dans g3 (bmatge/g3) |
| BDD | SQLite (existant), migration SQLAlchemy | Suffisant pour le POC, migration PostgreSQL facile si besoin |

## Modèle de données cible

### Modifications

| Modèle | Changement |
|--------|-----------|
| `ReferentielVersion` | Ajouter `cible` : `"organisation"` ou `"site"` |
| `Site` | **Nouveau** : id, nom, url, description, organisation_id → Entite |
| `Campagne` | Ajouter `cible` (redondant avec référentiel, pratique pour filtrage) |
| `Evaluation` | `entite_id` devient nullable, ajouter `site_id` nullable |
| `Score` | Élargir/supprimer la contrainte `CHECK (niveau BETWEEN 1 AND 4)` pour supporter N niveaux |
| `Dimension`, `Capacite`, `NiveauCritere` | Inchangés |

### Schéma

```
ReferentielVersion (cible: "organisation" | "site")
    └── Dimension
          └── Capacite (portee: C/D/P)
                └── NiveauCritere (1-N, flexible par référentiel)

Entite (type: SIRCOM/Bureau)
    ├── evaluations ──► Evaluation
    └── sites ──────►  Site
                         ├── nom, url, description
                         └── evaluations ──► Evaluation

Campagne (cible: "organisation" | "site", referentiel_id)
    └── Evaluation
          ├── entite_id (nullable) ── OU ── site_id (nullable)
          └── scores ──► Score ──► Capacite
```

### Contraintes

- `Evaluation` : exactement un des deux renseigné (`entite_id` XOR `site_id`)
- `Campagne.cible` doit correspondre à `Campagne.referentiel.cible`
- Un référentiel "site" ne peut être utilisé que pour évaluer des sites (et inversement)

## Chantiers

### 1. Migration du modèle de données
- [ ] Ajouter `cible` à `ReferentielVersion`
- [ ] Créer le modèle `Site`
- [ ] Modifier `Evaluation` (entite_id nullable, ajouter site_id)
- [ ] Ajouter `cible` à `Campagne`
- [ ] Migrer le seed existant : marquer le référentiel ComNum comme `cible="organisation"`
- [ ] Adapter les contraintes d'intégrité

### 2. Référentiels de test
- [ ] Rédiger un référentiel "Accessibilité" double portée (volet orga + volet site, ~10 critères chacun)
- [ ] Rédiger un référentiel "Design" double portée (~10 critères chacun)
- [ ] Rédiger un référentiel "Data" double portée (~10 critères chacun)
- [ ] Intégrer ces référentiels dans le seed

### 3. Vues sites
- [ ] Page liste des sites (CRUD)
- [ ] Formulaire création de site (lié à une organisation)
- [ ] Adaptation du formulaire d'évaluation (choix site ou organisation selon la campagne)
- [ ] Page résultats d'évaluation site
- [ ] Navigation : ajouter "Sites" au menu

### 4. Adaptation des vues existantes
- [ ] Dashboard : séparer ou filtrer par type de cible
- [ ] Page référentiel : navigation entre référentiels
- [ ] Campagnes : afficher le type de cible
- [ ] Évaluations : distinguer évaluations orga / site

### 5. (Futur) Corrélation sites → organisations
- [ ] Réflexion sur le modèle de corrélation
- [ ] Vue consolidée organisation (scores propres + scores agrégés des sites)
- [ ] Dashboard croisé

## Référentiels à créer (chantier 2)

Pour valider l'architecture, on crée 3 paires de mini-référentiels (~10 critères max chacun) :

| Domaine | Réf. Organisation | Réf. Site |
|---------|-------------------|-----------|
| **Accessibilité** | Processus, budget, formation, RH, pilotage | Score RGAA, conformité, audit, déclaration |
| **Design** | Charte, gouvernance, design system, UX research | Cohérence UI, responsive, parcours, performance |
| **Data** | Gouvernance data, compétences, culture, éthique | Analytics, qualité données, RGPD, open data |

Ces référentiels seront volontairement courts pour tester le modèle. Ils pourront être enrichis progressivement.
