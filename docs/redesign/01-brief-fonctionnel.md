# Brief fonctionnel — Outil de suivi de maturité numérique (maturity-model)

> Document de cadrage pour la refonte de l'UI. Il décrit ce que l'application **est** et **fait**
> d'un point de vue métier — pas comment elle est codée, ni à quoi elle ressemble aujourd'hui.
>
> Périmètre analysé : l'application web `webapp/` (la version vivante du produit). Le dépôt
> contient aussi deux prototypes antérieurs (questionnaire statique HTML/JS et prototype
> Streamlit, basés sur un ancien modèle à 33 questions / 4 axes) qui sont **hors périmètre**
> de la refonte : ils documentent l'histoire du produit, pas son présent.

---

## 1. Contexte & problème

Les organisations publiques — en premier lieu les services de communication ministériels
(SIRCOM et bureaux de communication des directions) et, par extension, les équipes MEF/MIWEB —
n'ont pas de moyen structuré de répondre à trois questions :

1. **Où en sommes-nous ?** Quel est le niveau de maturité de nos pratiques (communication
   numérique, design, accessibilité, data) et de nos sites web ?
2. **Où sont les écarts ?** Entre entités d'un même ministère, entre sites d'un même parc,
   entre le niveau actuel et le niveau visé.
3. **Progressons-nous ?** D'une campagne d'évaluation à l'autre, dans le temps.

Aujourd'hui ces évaluations, quand elles existent, se font dans des tableurs isolés (le
`Referentiel_Maturite_Design_MEF.xlsx` du dépôt en est l'exemple) : pas de consolidation,
pas d'historique, pas de comparaison possible. L'application transforme ces référentiels
d'expertise en un outil d'auto-évaluation outillé, répétable et comparable.

Le besoin a évolué en cours de route : parti d'un questionnaire unique sur la maturité de la
communication numérique d'une organisation, l'outil est devenu une **plateforme
multi-référentiels** capable d'évaluer aussi bien des **organisations** (pratiques, gouvernance,
compétences) que des **sites web** (conformité, qualité d'expérience), sur autant de
référentiels thématiques que nécessaire.

**Utilisateurs visés** : évaluateurs/consultants internes (qui conduisent les évaluations),
responsables d'entités (qui s'auto-évaluent), et pilotes transverses (qui comparent, suivent
et restituent). L'application ne distingue pas ces rôles aujourd'hui : tout utilisateur voit
et peut tout faire.

## 2. Proposition de valeur

Un outil unique qui héberge des **référentiels de maturité structurés** (dimensions →
capacités → niveaux décrits par des critères observables), permet d'**évaluer** des
organisations et des sites web sur ces référentiels au fil de **campagnes** répétées, et
**restitue** immédiatement les résultats : profil de maturité individuel, comparaison entre
entités, évolution dans le temps. La valeur centrale n'est pas le questionnaire, c'est le
référentiel : l'application est le véhicule qui le rend actionnable.

## 3. Le référentiel — l'actif central

### 3.1 Structure

Tout référentiel suit la même structure à quatre étages :

```
Référentiel (versionné, ciblé "organisation" OU "site")
  └── Dimension (numérotée, nommée, décrite)          ex. « 3. Design & cohérence »
        └── Capacité (numéro x.y, nom, description,   ex. « 3.4 Accessibilité »
            portée C/D/P)
              └── Niveau (1..N, nom + critère          ex. « 3 — Intégré : accessibilité
                  descriptif détaillé)                  intégrée dès la conception… »
```

- **Le nombre de niveaux est flexible par référentiel** : 4 niveaux pour les référentiels
  « organisation » historiques (Émergent → Structuré → Intégré → Pérenne), 3 niveaux pour les
  référentiels dérivés du référentiel Design MEF/MIWEB (Absent → Engagé → Systématisé côté
  organisation ; Insuffisant → Partiel → Conforme côté site). Les noms de niveaux sont propres
  à chaque référentiel.
- **Chaque niveau de chaque capacité porte un critère rédigé** : une description concrète et
  observable de ce à quoi ressemble la pratique à ce niveau. C'est ce texte que l'évaluateur
  lit pour choisir son niveau — il n'y a pas de « question », le critère est la question.
- **La portée** (C / D / P) qualifie chaque capacité : dans le référentiel d'origine,
  C = Centrale (pilotée par le SIRCOM), D = Distribuée (exercée par les bureaux),
  P = Partagée (coordination nécessaire). Elle est informative et sert de filtre de
  consultation ; elle n'influe pas sur le calcul des scores.
- La philosophie des échelles à 4 niveaux est la **pérennité** : la progression n'est pas
  « faire plus » mais « construire plus durable » (du savoir porté par des individus vers un
  système qui se maintient et évolue de lui-même).

### 3.2 Les référentiels embarqués (volumétrie)

Sept référentiels sont livrés avec l'application :

| Référentiel | Cible | Dimensions | Capacités | Niveaux | Critères |
|---|---|---|---|---|---|
| **ComNum v2.0** (actif par défaut) | Organisation | 7 | 44 | 4 | 176 |
| **Design-org-v1** (MEF/MIWEB) | Organisation | 4 | 15 | 3 | 45 |
| **Design-site-v1** (MEF/MIWEB) | Site | 2 | 11 | 3 | 33 |
| Accessibilité-org-v1 | Organisation | 2 | 8 | 4 | 32 |
| Accessibilité-site-v1 | Site | 2 | 7 | 3 | 21 |
| Data-org-v1 | Organisation | 2 | 6 | 4 | 24 |
| Data-site-v1 | Site | 2 | 6 | 3 | 18 |
| **Total** | | **21** | **97** | | **349** |

- **ComNum v2.0** est le référentiel historique complet : 7 dimensions (Vision &
  positionnement, Connaissance des publics, Design & cohérence, Écosystème éditorial,
  Corpus & patrimoine éditorial, Production & organisation, Outillage & infrastructure).
  Il est documenté en profondeur dans `referentiel-v2.md` (structure, mapping avec l'ancien
  modèle à 33 questions) et `criteres-detailles.md` (critères longs + « signaux observables »
  par capacité).
- **Design-org-v1 / Design-site-v1** forment le référentiel Design MEF/MIWEB « 15 + 11 » :
  côté organisation, 4 dimensions (Recherche utilisateur, Conception & prototypage,
  Évaluation & amélioration continue, Gouvernance design) ; côté site, 2 dimensions
  (Conformité & standards — DSFR, agrément SIG, responsive, mentions légales — et Qualité de
  l'expérience utilisateur). Sa source d'expertise est le classeur
  `Referentiel_Maturite_Design_MEF.xlsx` (onglets : Référentiel, Journal UX, Tables de
  référence, Guide de scoring), dont seule la partie « critères scorables » est reprise
  dans l'application.
- Les paires Accessibilité et Data sont des référentiels courts créés pour valider
  l'architecture multi-référentiels ; ils ont vocation à être enrichis.

### 3.3 Comment le référentiel pilote l'application

Le référentiel n'est pas un paramètre : il **détermine tout**. Le choix d'un référentiel à la
création d'une évaluation fixe la cible autorisée (organisation ou site), le contenu du
formulaire de saisie (toutes ses capacités, groupées par dimension), l'échelle de notation
(son nombre et ses noms de niveaux), et les axes de toutes les restitutions (les dimensions
sont les axes des radars, les capacités les colonnes des heatmaps). Ajouter un référentiel
ajoute de fait un nouveau « produit d'évaluation » complet sans autre changement.

## 4. Périmètre fonctionnel actuel

### 4.1 Consultation du référentiel — **complet**

Une page présente n'importe quel référentiel dans son intégralité : sélecteur pour passer d'un
référentiel à l'autre, dimensions en accordéons, et pour chaque capacité le détail des
critères de chaque niveau. Deux outils d'exploration : recherche plein texte sur les capacités
(numéro, nom, description) et filtre par portée (C/D/P). Quand des évaluations validées
existent sur ce référentiel, le score moyen constaté de chaque capacité est affiché en regard,
ce qui fait de la page à la fois une documentation et un état des lieux.

### 4.2 Gestion des organisations (« entités ») — **partiel**

Création (nom, type SIRCOM/Bureau, direction de rattachement, description), liste avec le
dernier score global obtenu par référentiel (valeur, maximum, pourcentage), suppression (qui
emporte les évaluations liées). **Pas de modification** d'une entité existante. Cinq entités
de démonstration sont pré-chargées.

### 4.3 Gestion des sites web — **partiel**

Même logique : création (nom, URL, description, organisation de rattachement obligatoire),
liste avec derniers scores par référentiel, suppression en cascade. Pas de modification.
Quatre sites de démonstration pré-chargés. Le site appartient toujours à une organisation,
ce qui prépare (sans l'implémenter) la consolidation des scores sites vers l'organisation.

### 4.4 Campagnes d'évaluation — **partiel**

Une campagne est une fenêtre temporelle nommée (label, date de début, date de fin optionnelle,
statut en cours / terminée) qui regroupe des évaluations d'organisations pour permettre les
comparaisons « à date ». Création, liste, suppression (en cascade sur les évaluations).
Limites actuelles : le statut « terminée » n'est modifiable par aucun écran (une campagne
reste « en cours » à vie), et les campagnes ne concernent en pratique que les évaluations
d'organisations — les évaluations de sites se font hors campagne.

### 4.5 Réalisation d'une évaluation — **complet**

Le cœur de l'outil, en trois temps :

1. **Création** : choix du référentiel, puis de la cible (une organisation ou un site, selon
   la cible du référentiel), rattachement optionnel à une campagne en cours (organisations
   uniquement), saisie du nom de l'évaluateur.
2. **Saisie** : formulaire unique présentant toutes les capacités groupées par dimension.
   Pour chaque capacité, l'évaluateur lit les critères des N niveaux et sélectionne celui qui
   décrit le mieux la situation ; il peut ajouter une justification libre (signaux observés).
   Une barre de progression et un compteur suivent l'avancement ; une navigation par dimension
   permet de circuler dans le formulaire. La saisie peut être **sauvegardée en brouillon**
   et reprise (les réponses sont pré-remplies).
3. **Validation** : possible uniquement quand 100 % des capacités sont scorées. La validation
   fige la date d'évaluation, fait basculer le statut de « brouillon » à « validée » et ouvre
   la page de résultats. Seules les évaluations validées alimentent les statistiques.

Une liste globale des évaluations (toutes cibles, tous statuts) permet de reprendre un
brouillon, consulter des résultats ou supprimer une évaluation.

### 4.6 Restitution individuelle d'une évaluation — **complet**

Pour une évaluation validée : score global (avec jauge en pourcentage du maximum), score par
dimension (graphique en barres + barres de progression détaillées), profil radar sur les
dimensions, et tableau exhaustif capacité par capacité (dimension, portée, niveau attribué,
justification saisie). Liens de rebond vers l'évolution de l'entité et le tableau de bord de
la campagne.

### 4.7 Tableau de bord de campagne (comparaison inter-entités) — **complet**

Pour une campagne donnée, à partir de ses évaluations validées : statistiques par dimension
(moyenne, écart-type, min, max, nombre d'entités), radar comparatif superposant chaque entité
et la moyenne du groupe, graphique moyennes / écarts-types, et **heatmap entités × capacités**
donnant la lecture fine des forces et faiblesses de chacun. C'est la vue « pilote transverse ».

### 4.8 Évolution d'une organisation dans le temps — **complet**

Pour une organisation, l'historique de ses évaluations validées est regroupé **par
référentiel** : courbes d'évolution de chaque dimension au fil des campagnes (ou des dates
pour les évaluations hors campagne), et radar de la dernière évaluation. Permet de répondre à
« progressons-nous ? » référentiel par référentiel. Pas d'équivalent pour les sites.

### 4.9 Tableau de bord d'accueil — **complet**

Vue d'ensemble à l'ouverture : six indicateurs clés (nombre d'organisations, de sites, de
référentiels, d'évaluations validées, de campagnes, score moyen global avec seuils de
couleur), radar du profil de maturité moyen (organisations), classement des entités et des
sites par score, accès rapides aux campagnes et aux fiches.

### 4.10 API de données — **partiel**

Quatre points d'accès JSON en lecture exposent les données agrégées (indicateurs du tableau
de bord, scores par organisation, scores par site, scores d'une évaluation). Ils servent
aujourd'hui les composants graphiques de l'application elle-même ; il n'y a ni API d'écriture,
ni documentation, ni contrôle d'accès.

### 4.11 Données de démonstration — **complet (mais structurel)**

Au premier démarrage, l'application se peuple automatiquement : les 7 référentiels, 5 entités
et 4 sites de démonstration. C'est aussi, de fait, **le seul mécanisme d'administration du
référentiel** (voir § 7).

## 5. Modèle de données conceptuel

Huit objets métier :

- **Référentiel** (versionné) : un cadre d'évaluation nommé (ex. « ComNum v2.0 »), avec une
  description, une **cible** (organisation ou site) et un indicateur « actif » (référentiel
  mis en avant par défaut). Contient des dimensions.
- **Dimension** : un axe d'analyse numéroté du référentiel. Contient des capacités.
- **Capacité** : l'unité évaluable (numéro x.y, nom, description, portée C/D/P). Contient ses
  niveaux.
- **Niveau / critère** : pour une capacité, la description rédigée d'un palier de maturité
  (numéro, nom du palier, critère détaillé, et un champ « signaux observables » prévu mais
  non alimenté).
- **Organisation (entité)** : la structure évaluée (nom, type SIRCOM ou Bureau, direction,
  description). Possède des sites et des évaluations.
- **Site** : un site web (nom, URL, description), **toujours rattaché à une organisation**.
  Possède ses propres évaluations.
- **Campagne** : une vague d'évaluation datée (label, début, fin, statut). Regroupe des
  évaluations pour comparaison synchrone.
- **Évaluation** : l'acte d'évaluer **une cible** (une organisation OU un site, exclusivement)
  **sur un référentiel**, à une date, par un évaluateur, avec un statut (brouillon / validée),
  optionnellement dans une campagne, et un commentaire global (champ prévu, non exposé).
  Contient des **scores**.
- **Score (réponse)** : pour une évaluation et une capacité données, le niveau retenu et sa
  justification libre (plus un champ « signaux constatés » prévu, non exposé). Une seule
  réponse par capacité et par évaluation.

Relations en une phrase : *un référentiel structure des dimensions qui regroupent des
capacités déclinées en niveaux ; une organisation possède des sites ; une évaluation applique
un référentiel à une organisation ou à un site, éventuellement dans le cadre d'une campagne,
et enregistre un score par capacité.*

## 6. Règles métier clés

- **Notation** : le score d'une capacité est le niveau choisi (entier de 1 au maximum du
  référentiel). Pas de « non applicable », pas de demi-niveaux, pas de pondération — toutes
  les capacités pèsent pareil, la portée C/D/P n'influe pas.
- **Score de dimension** = moyenne arithmétique des scores de ses capacités (arrondi à 2
  décimales). C'est une valeur continue : l'application ne calcule pas de « niveau atteint »
  par règle de palier (pas de logique « niveau 3 atteint si toutes les capacités ≥ 3 »).
- **Score global d'une cible** = moyenne des moyennes de dimension (chaque dimension pèse
  pareil quel que soit son nombre de capacités). ⚠️ Exception : la page de résultats d'une
  évaluation calcule le score global comme moyenne directe de toutes les capacités — les deux
  règles divergent quand les dimensions sont de tailles inégales (voir § 8).
- **Pourcentage de maturité** = score / niveau maximum du référentiel (le maximum est déduit
  dynamiquement de l'échelle du référentiel : 3 ou 4).
- **Seules les évaluations validées comptent** dans tous les agrégats (moyennes de campagne,
  scores affichés sur les fiches, radars, API). Les brouillons sont invisibles des
  statistiques.
- **Validation** : une évaluation ne peut être validée que si toutes les capacités du
  référentiel sont scorées ; la validation horodate l'évaluation.
- **Agrégats de campagne** : pour chaque dimension, moyenne, écart-type, min et max des
  scores de dimension des évaluations validées de la campagne.
- **« Dernier score » d'une cible** : pour chaque référentiel, on retient la plus récente
  évaluation validée (une cible peut donc afficher plusieurs scores, un par référentiel).
- **Intégrité** : une évaluation porte sur exactement une cible (organisation XOR site) ;
  un référentiel « site » ne peut évaluer que des sites et réciproquement ; une seule
  réponse par capacité et par évaluation ; supprimer une cible ou une campagne supprime ses
  évaluations et leurs réponses.

## 7. Hors périmètre / non implémenté

Utile pour cadrer la refonte — l'application **ne fait pas** aujourd'hui :

- **Comptes, authentification, rôles** : aucun. Tout visiteur voit tout et peut tout faire
  (créer, évaluer, supprimer). L'« évaluateur » est un simple champ texte déclaratif.
- **Administration du référentiel** : aucune interface de création/édition de référentiels,
  dimensions, capacités ou critères. Les référentiels ne vivent que dans le code
  d'initialisation ; les enrichir suppose une intervention technique. Pas d'import du
  classeur Excel, pas de gestion de cycle de vie des versions (v2.0 → v2.1) au-delà du champ
  « actif ».
- **Modification** des organisations, sites et campagnes après création (création et
  suppression uniquement) ; pas de clôture de campagne.
- **Export / restitution portable** : aucun export CSV, Excel ou PDF, aucune vue imprimable.
  Les résultats ne sortent de l'outil que par capture d'écran.
- **Plan d'action** : l'outil constate la maturité mais ne propose ni recommandations, ni
  cibles à atteindre, ni suivi d'actions correctives ; le champ « signaux observables » des
  critères et le « guide de scoring » du classeur Excel ne sont pas repris.
- **Consolidation sites → organisation** : le lien hiérarchique existe, mais les scores des
  sites ne remontent pas dans la maturité de leur organisation (explicitement différé dans
  l'epic multi-référentiel). Pas non plus de vue « évolution » pour un site.
- **Comparaison inter-campagnes** directe (delta entre deux campagnes) : l'évolution ne se
  lit que par organisation.
- **Collaboration** : pas d'évaluation à plusieurs, pas de workflow de relecture/validation
  par un tiers, pas de commentaires, pas de notifications.
- **Questionnaire public d'auto-évaluation anonyme** : la version actuelle suppose des cibles
  déclarées à l'avance ; le mode « je réponds et je vois mon score » sans création préalable
  (celui des prototypes v1) n'existe plus.

## 8. Découvertes & incohérences à trancher lors de la refonte

Constats factuels relevés pendant l'analyse, à arbitrer :

1. **Deux définitions du score global** coexistent : moyenne de toutes les capacités (page de
   résultats d'une évaluation) vs moyenne des moyennes de dimension (fiches, API, tableaux de
   bord). Les valeurs divergent dès que les dimensions n'ont pas le même nombre de capacités
   (cas de tous les référentiels). Une seule règle devra être retenue.
2. **La légende de la portée C/D/P diverge** entre le référentiel documentaire
   (C = Centrale, D = Distribuée, P = Partagée) et l'interface de consultation
   (« C — Cabinet, D — Direction, P — Publique »). La source documentaire fait foi.
3. Les champs **« signaux observables »** (par critère), **« signaux constatés »** et
   **« commentaire global »** (par évaluation) existent dans le modèle mais ne sont ni saisis
   ni affichés — alors que `criteres-detailles.md` fournit les signaux observables pour les
   44 capacités du référentiel ComNum. Gisement fonctionnel immédiat.
4. Les **critères embarqués sont des versions abrégées** de ceux de `criteres-detailles.md`
   (texte raccourci, signaux omis) ; le classeur Excel Design contient un « guide de scoring »
   et des tables de référence non repris. Le référentiel « riche » n'est donc que
   partiellement dans l'outil.
5. Le **statut de campagne « terminée » est inatteignable** depuis l'interface, et la
   protection contre les **évaluations en doublon** (message « une évaluation similaire
   existe déjà ») repose sur une contrainte qui n'existe pas en base : on peut créer
   plusieurs évaluations identiques (même cible, même référentiel, même campagne).
6. L'écran de saisie affiche systématiquement une ligne « Campagne : » même pour les
   évaluations hors campagne (sites notamment), où elle reste vide.
7. Le dépôt contient **trois générations d'application** (front statique + Streamlit sur
   l'ancien modèle 33 questions / 4 axes, puis l'application web actuelle) ; l'ancien
   `data.json` et le questionnaire embarqué dans `script.js` ont d'ailleurs divergé entre eux.
   La refonte est l'occasion d'archiver les deux premières.
