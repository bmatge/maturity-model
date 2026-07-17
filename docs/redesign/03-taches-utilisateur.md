# 03 — Tâches utilisateur

> Inventaire exhaustif des tâches que l'application doit permettre de réaliser, du point de vue de l'utilisateur.
> Base de conception pour la nouvelle UI (pages et parcours). Ce document décrit le **QUOI** (fonctions + données), jamais le **COMMENT** visuel.

**Sources analysées** : `webapp/app.py` (toutes les routes), `webapp/models.py`, `webapp/seed.py`, les 13 templates de `webapp/templates/`, le POC statique historique (`index.html`, `questions.html`, `results.html`, `script.js`, `data.json`, `app.py` Streamlit), `referentiel-v2.md`, `criteres-detailles.md`, `tasks/epic-multi-referentiel.md`.

---

## Objets métier manipulés

| Objet | Description | Attributs clés |
|---|---|---|
| **Référentiel** (version) | Un référentiel de maturité versionné, typé par cible | label, description, cible (`organisation` \| `site`), actif/inactif, échelle propre (3 ou 4 niveaux, noms de niveaux variables : Émergent→Pérenne, Insuffisant→Conforme, Absent→Systématisé…) |
| **Dimension** | Regroupement thématique du référentiel (ex. « Vision & positionnement ») | numéro, nom, description |
| **Capacité** | Unité évaluable (ex. « 1.1 Vision stratégique ») | numéro, nom, description, portée (C/D/P) |
| **Niveau / critère** | Description d'un niveau de maturité pour une capacité | niveau (1–N), nom, description, signaux observables |
| **Entité** (organisation) | Organisation évaluable (SIRCOM, bureau de com) | nom, type (SIRCOM/Bureau), direction, description |
| **Site** | Site web rattaché à une organisation | nom, URL, description, organisation de rattachement |
| **Campagne** | Vague d'évaluation datée regroupant des évaluations | label, date début, date fin, statut (`en_cours`/`terminee`) |
| **Évaluation** | Une passation : une cible (entité XOR site) × un référentiel, éventuellement rattachée à une campagne | référentiel, cible, campagne (optionnelle), évaluateur, date, statut (`brouillon`/`validee`), commentaire global |
| **Score** (réponse) | Le niveau attribué à une capacité dans une évaluation | niveau, justification, signaux constatés |
| **Résultats calculés** | Agrégats dérivés (jamais saisis) | moyenne par dimension, score global, moyenne/écart-type/min/max par dimension au niveau campagne, moyenne par capacité, % du niveau max, séries temporelles |

Référentiels actuellement embarqués : ComNum v2.0 (7 dim., 44 cap., 4 niveaux), Accessibilité-org-v1 (8 cap.), Accessibilité-site-v1 (7 cap., 3 niveaux), **Design-org-v1 (15 cap., 4 dim., 3 niveaux)**, **Design-site-v1 (11 cap., 3 niveaux)**, Data-org-v1 (6 cap.), Data-site-v1 (6 cap.).

---

## Vue d'ensemble — 5 groupes de tâches

| # | Groupe | Intention utilisateur | Nb de tâches |
|---|---|---|---|
| A | **Découvrir et consulter le référentiel** | Comprendre ce qu'on mesure : dimensions, capacités, niveaux, critères | 6 |
| B | **S'évaluer (répondre)** | Réaliser une évaluation de bout en bout : démarrer, répondre, justifier, reprendre, valider | 10 |
| C | **Piloter une campagne** | Organiser une vague d'évaluation, suivre l'avancement, la clôturer | 9 |
| D | **Analyser et restituer les résultats** | Lire, comparer, suivre dans le temps, partager les scores | 11 |
| E | **Administrer le patrimoine évalué et les référentiels** | Gérer les entités, les sites, les référentiels eux-mêmes | 11 |
| | **Total** | | **47** |

Légende « Existant » : ✅ complet · 🟡 partiel (fonction présente mais incomplète ou mal outillée) · ❌ absent mais nécessaire.

---

## A — Découvrir et consulter le référentiel

L'utilisateur (répondant comme pilote) doit pouvoir comprendre l'instrument de mesure avant et pendant l'évaluation.

| Tâche | Données manipulées | Existant | Fréquence | Notes |
|---|---|---|---|---|
| A1. Comprendre le principe de l'outil et l'échelle de maturité (à quoi ça sert, ce que veulent dire les niveaux) | échelle de niveaux, noms de niveaux, principe de progression (pérennité) | 🟡 | une fois (première visite) | Le POC statique historique a une page d'intro pédagogique ; la webapp Flask n'a aucun texte d'accueil expliquant la démarche. L'échelle varie selon le référentiel (3 ou 4 niveaux, noms différents) — la pédagogie doit être contextuelle. |
| A2. Choisir le référentiel à consulter parmi ceux disponibles | référentiel (label, cible, description) | ✅ | par campagne | Sélecteur sur la page référentiel (`?ref_id=`). 7 référentiels en base. |
| A3. Parcourir un référentiel : dimensions → capacités → niveaux/critères | dimension, capacité, niveau/critère, portée | ✅ | par campagne | Accordéons imbriqués. Les « signaux observables » existent dans le modèle (`NiveauCritere.signaux_observables`) mais ne sont ni seedés ni affichés — donnée prévue, non exploitée. |
| A4. Rechercher une capacité par mot-clé | capacité (numéro, nom, description) | ✅ | quotidien pendant campagne | Recherche plein-texte côté client. |
| A5. Filtrer les capacités par portée (C / D / P) | capacité (portée) | ✅ | par campagne | Un bureau de com veut ne voir que les capacités D et P qui le concernent. NB : la portée n'est PAS utilisée pour filtrer le questionnaire d'évaluation (voir B4). |
| A6. Voir, pour chaque capacité, le score moyen constaté sur les évaluations validées | capacité, scores agrégés | ✅ | par campagne | Badge « Moy. x/4 » — croise référentiel et résultats ; utile au pilote, bruit potentiel pour un répondant. |

---

## B — S'évaluer (répondre au questionnaire)

Le cœur de l'outil : une évaluation = une cible × un référentiel, remplie capacité par capacité.

| Tâche | Données manipulées | Existant | Fréquence | Notes |
|---|---|---|---|---|
| B1. Démarrer une évaluation : choisir le référentiel, puis la cible compatible (entité ou site selon la cible du référentiel), éventuellement la rattacher à une campagne en cours, s'identifier comme évaluateur | évaluation (référentiel, entité XOR site, campagne, évaluateur) | ✅ | par campagne | Contrainte : cible du référentiel ⇒ type de cible. Le rattachement campagne n'existe que pour les évaluations d'organisations (les évaluations de sites sont toujours « hors campagne » — limite actuelle du code). Doublon détecté → message et renvoi vers la liste. |
| B2. Répondre pour une capacité : lire les descriptions des niveaux et choisir celui qui correspond | score (niveau), niveau/critère | ✅ | quotidien pendant campagne | Choix par cartes radio, 1 réponse par capacité, échelle propre au référentiel. |
| B3. Justifier une réponse (préciser les signaux observés) | score (justification, signaux constatés) | 🟡 | quotidien pendant campagne | Champ texte libre « justification » présent. Le champ `signaux_constates` du modèle Score n'a aucune UI. Pas de pièce jointe / lien de preuve. |
| B4. Ne répondre qu'aux capacités qui concernent mon entité (portée C/D/P), ou marquer une capacité « non applicable » | capacité (portée), score | ❌ | par campagne | Aujourd'hui le formulaire présente toutes les capacités à tout le monde ; une capacité sans réponse est simplement absente des scores. Le référentiel définit pourtant des portées (C = central, D = distribué, P = partagé) faites pour ça. Nécessaire pour que le score d'un bureau ne soit pas pollué par des capacités purement SIRCOM. |
| B5. Suivre sa progression dans le questionnaire (combien de capacités répondues / restantes, naviguer par dimension) | scores saisis, dimensions | ✅ | quotidien pendant campagne | Barre de progression + compteur x/N + ancres par dimension. |
| B6. Sauvegarder un brouillon en cours de route | évaluation (statut brouillon), scores | ✅ | quotidien pendant campagne | Bouton « Sauvegarder le brouillon » ; les réponses pré-remplissent à la reprise. |
| B7. Reprendre une évaluation en cours (retrouver son brouillon) | évaluation (statut), scores existants | 🟡 | quotidien pendant campagne | Possible via la liste des évaluations (« Compléter ») ou le dashboard campagne (« Continuer ») — mais rien ne ramène directement le répondant à « mon évaluation en cours » (pas de notion d'utilisateur, voir E11). |
| B8. Corriger une réponse avant validation | score (niveau, justification) | ✅ | quotidien pendant campagne | Re-sélection d'un niveau, écrase l'existant. |
| B9. Valider (soumettre) l'évaluation — la figer et la faire compter dans les agrégats | évaluation (statut validee, date), scores | 🟡 | par campagne | Bouton « Valider l'évaluation » → statut `validee`, horodatage, redirection vers les résultats. Seules les évaluations validées comptent dans tous les agrégats. Manque : contrôle de complétude (on peut valider avec 0 réponse), et récapitulatif avant validation. |
| B10. Corriger une évaluation déjà validée / la repasser en brouillon | évaluation (statut), scores | 🟡 | par campagne (rare) | Le formulaire de saisie reste techniquement accessible après validation et re-valider écrase les scores (en changeant la date), mais il n'existe aucun concept explicite de « rouvrir » ; risque d'écrasement silencieux. À formaliser : qui peut corriger, et trace de la modification. |

Tâche connexe héritée du POC statique (à arbitrer) : **auto-test anonyme sans compte ni enregistrement** (répondre aux questions, voir son radar, ne rien persister) — c'était tout le produit v1 (33 questions / 4 axes, réponses en localStorage) ; non repris dans la webapp.

---

## C — Piloter une campagne

Une campagne = une vague d'évaluation datée qui regroupe les évaluations de plusieurs entités pour permettre la comparaison et le suivi dans le temps.

| Tâche | Données manipulées | Existant | Fréquence | Notes |
|---|---|---|---|---|
| C1. Créer une campagne (nom, dates de début/fin) | campagne (label, date_debut, date_fin) | ✅ | par campagne (1×) | La campagne n'est plus liée à un référentiel à la création (le référentiel se choisit à l'évaluation) ; les évaluations d'une même campagne sont censées partager le même référentiel mais rien ne le garantit. |
| C2. Consulter la liste des campagnes (actives et passées) et leur statut | campagne, nb d'évaluations | ✅ | par campagne | Liste triée par date. |
| C3. Définir le périmètre d'une campagne : quelles entités sont attendues (invitées) | campagne, entités attendues | ❌ | par campagne (1×) | Aucune notion de « participants attendus » : une campagne ne contient que les évaluations effectivement démarrées. Impossible de distinguer « n'a pas commencé » de « pas concerné ». Prérequis du suivi d'avancement (C5) et de la relance (C6). |
| C4. Inviter / donner accès aux répondants (transmettre à chaque entité le lien vers son évaluation) | campagne, entité, évaluation, répondant | ❌ | par campagne (1×) | Aujourd'hui le circuit est entièrement manuel et hors outil (le répondant doit lui-même créer son évaluation en choisissant les bons référentiel/campagne/entité — source d'erreurs et de doublons). |
| C5. Suivre l'avancement de la campagne : qui a validé, qui est en brouillon, qui n'a pas commencé | campagne, évaluations (statut), entités | 🟡 | quotidien pendant campagne | Le dashboard campagne liste les évaluations existantes avec badge Brouillon/Validée et actions Continuer/Résultats — mais sans périmètre attendu (C3), pas de « manquants » ni de taux de participation. |
| C6. Relancer les entités en retard | campagne, entités sans évaluation validée | ❌ | quotidien pendant campagne | Dépend de C3/C4. Même sans email automatique, il faut au minimum la liste des retardataires à copier. |
| C7. Clôturer une campagne (la passer « terminée », figer les résultats) | campagne (statut, date_fin) | ❌ | par campagne (1×) | Le champ `statut` (`en_cours`/`terminee`) existe en base et conditionne la liste des campagnes proposées à la création d'évaluation — mais **aucune action ne permet de changer ce statut**. Une campagne reste « en cours » pour toujours. Corollaire : rouvrir une campagne clôturée. |
| C8. Modifier une campagne (renommer, ajuster les dates) | campagne (label, dates) | ❌ | par campagne (rare) | Seules création et suppression existent. |
| C9. Supprimer une campagne (et ses évaluations) | campagne, évaluations, scores | ✅ | rare | Modale de confirmation ; suppression en cascade des évaluations. Destructif, à réserver à un rôle pilote/admin. |

---

## D — Analyser et restituer les résultats

Trois niveaux de lecture : une évaluation, une campagne (comparaison inter-entités), une entité dans le temps (comparaison inter-campagnes).

| Tâche | Données manipulées | Existant | Fréquence | Notes |
|---|---|---|---|---|
| D1. Consulter les résultats d'une évaluation : score par dimension (radar, jauges), niveau atteint, détail capacité par capacité avec justifications | évaluation, scores, moyennes par dimension | ✅ | par campagne | Radar DSFR Chart + tableau détaillé (dimension, capacité, portée, niveau, justification). |
| D2. Consulter le tableau de bord global : indicateurs clés (nb d'organisations, sites, référentiels, évaluations validées, campagnes, score moyen), radar moyen, classement des entités | agrégats globaux, entités, campagnes, sites | ✅ | quotidien pendant campagne | Page d'accueil + API JSON (`/api/dashboard`, `/api/entites/scores`, `/api/sites/scores`). Scopé aux évaluations d'organisations pour les graphiques. |
| D3. Consulter le tableau de bord d'une campagne : moyenne, écart-type, min/max par dimension | campagne, stats par dimension | ✅ | quotidien pendant campagne | Tuiles + bar chart moyenne/écart-type. |
| D4. Comparer les entités d'une campagne entre elles (radar superposé, moyenne de la campagne en référence) | évaluations validées de la campagne, scores par dimension | ✅ | par campagne | Radar comparatif : une série par entité + série « Moyenne ». |
| D5. Repérer les forces/faiblesses fines : heatmap entités × capacités | scores par capacité et par entité | ✅ | par campagne | Tableau coloré par niveau. Devient illisible au-delà de ~44 colonnes — contrainte à traiter dans la nouvelle UI. |
| D6. Suivre l'évolution d'une entité dans le temps (à travers les campagnes), par référentiel | entité, évaluations validées historisées, séries temporelles par dimension | ✅ | par campagne | Page « Évolution » : courbes par dimension + radar de la dernière évaluation, groupés par référentiel (une entité peut être suivie sur ComNum ET Design ET Data). |
| D7. Comparer deux entités hors campagne, ou deux campagnes entre elles (progression globale d'une vague à l'autre) | évaluations, campagnes, scores agrégés | ❌ | par campagne | La comparaison n'existe qu'à l'intérieur d'une campagne (D4). Comparer T1 vs T2 au niveau global, ou entité A vs entité B librement, n'est pas outillé. |
| D8. Consulter la synthèse multi-référentiels d'une entité ou d'un site (son score sur chaque référentiel : ComNum, Design, Accessibilité, Data) | entité/site, dernière évaluation validée par référentiel, % du niveau max | ✅ | par campagne | Jauges par référentiel sur les listes entités/sites (le % normalise les échelles 3 vs 4 niveaux). |
| D9. Voir les résultats des sites d'une organisation, rapprochés de ceux de l'organisation | site, organisation, scores | 🟡 | par campagne | Les scores des sites existent (liste sites), mais aucune vue ne rapproche une organisation de ses sites (la vision cible de l'epic prévoit que les scores sites qualifient la maturité de l'organisation). Pas de page « fiche entité » consolidée. |
| D10. Exporter / partager une restitution (rapport d'évaluation, synthèse de campagne — PDF, tableur, lien) | évaluation, campagne, scores | ❌ | par campagne | Aucun export. Or la restitution en comité (COPIL, direction) est la finalité de l'exercice ; aujourd'hui il faut faire des captures d'écran. Un export tableur des scores bruts (entités × capacités) est aussi nécessaire pour retraitement. |
| D11. Dériver un plan d'action des résultats (identifier les capacités prioritaires, viser un niveau cible) | scores, capacités, niveaux cibles, écarts | ❌ | par campagne | Intention présente dès le POC v1 (lien « voir le plan d'action » commenté dans `results.html`). Le référentiel s'y prête (le niveau N+1 de chaque capacité décrit l'étape suivante). Au minimum : mettre en évidence les capacités les plus faibles ; au mieux : fixer des cibles et suivre l'écart. |

---

## E — Administrer le patrimoine évalué et les référentiels

| Tâche | Données manipulées | Existant | Fréquence | Notes |
|---|---|---|---|---|
| E1. Créer une entité (organisation) | entité (nom, type, direction, description) | ✅ | rare | Formulaire dédié. |
| E2. Modifier une entité | entité | ❌ | rare | Aucune route d'édition — une faute de frappe dans un nom oblige à supprimer (et perdre les évaluations) ou à vivre avec. |
| E3. Supprimer une entité (et son historique d'évaluations) | entité, évaluations, scores, sites rattachés | ✅ | rare | Confirmation modale ; cascade sur évaluations + scores + sites. Très destructif — à protéger par rôle. |
| E4. Créer un site et le rattacher à une organisation | site (nom, URL, description, organisation) | ✅ | rare | Le rattachement est obligatoire. |
| E5. Modifier un site (URL, description, rattachement) | site | ❌ | rare | Même lacune que E2. |
| E6. Supprimer un site (et ses évaluations) | site, évaluations, scores | ✅ | rare | Confirmation modale, cascade. |
| E7. Consulter la liste des référentiels disponibles (label, cible, nb de dimensions/capacités, échelle) | référentiel | 🟡 | rare | Visible seulement via le sélecteur de la page Référentiel ; pas de vue de gestion. |
| E8. Créer / importer un nouveau référentiel ou une nouvelle version (dimensions, capacités, niveaux, portées) | référentiel, dimensions, capacités, niveaux/critères | ❌ | une fois / rare | Aujourd'hui tout référentiel s'ajoute **en modifiant `seed.py`** (c'est ainsi que le référentiel Design MEF/MIWEB a été ajouté). Le contenu existe par ailleurs en Markdown (`referentiel-v2.md`, `criteres-detailles.md`) et en Excel (`Referentiel_Maturite_Design_MEF.xlsx`) — un import structuré (tableur/JSON) est le besoin réel. |
| E9. Modifier un référentiel (corriger un libellé de critère, compléter les signaux observables) et gérer ses versions | référentiel, capacités, niveaux/critères | ❌ | rare | Aucune édition. Règle métier : un référentiel déjà utilisé par des évaluations validées ne doit pas être modifié silencieusement → versionnage (le modèle s'appelle déjà `ReferentielVersion`). |
| E10. Activer / désactiver un référentiel (lequel est proposé par défaut, lesquels sont ouverts à l'évaluation) | référentiel (is_active) | ❌ | rare | Le drapeau `is_active` existe et pilote le référentiel par défaut du dashboard, mais rien ne permet de le changer. Désactiver un référentiel obsolète sans le supprimer est nécessaire. |
| E11. Gérer les utilisateurs et leurs rôles (répondant, pilote, lecteur, admin) et restreindre les actions destructives | utilisateur, rôle, périmètre (entité) | ❌ | une fois | Aucune authentification : tout visiteur peut tout supprimer. Le champ `evaluateur` est un texte libre déclaratif. C'est la condition de « mon évaluation » (B7), des invitations (C4) et de la protection des suppressions (C9, E3, E6). |

---

## Enchaînements critiques

Les séquences qui doivent être fluides dans la nouvelle UI, avec les données qui passent d'une étape à l'autre.

### 1. Cycle de vie complet d'une campagne (parcours pilote + répondants)

```
Créer la campagne ──► Définir le périmètre ──► Inviter les répondants ──► Chaque entité s'évalue ──► Suivre l'avancement ──► Clôturer ──► Restituer
   (C1)                  (C3 ❌)                  (C4 ❌)                    (B1→B9)                  (C5 🟡)              (C7 ❌)      (D3–D5, D10 ❌)
```

Données transmises : la **campagne** (id, label, référentiel implicite) est créée par le pilote → le périmètre lie campagne × **entités attendues** → l'invitation porte campagne + entité + référentiel pré-choisis vers le répondant (aujourd'hui le répondant doit re-sélectionner les trois à la main, principale source d'erreurs) → chaque **évaluation validée** alimente les **agrégats de campagne** (moyenne, écart-type, heatmap) → la clôture fige le tout pour la restitution.

### 2. Passation d'une évaluation (parcours répondant)

```
Arriver sur son évaluation ──► Comprendre l'échelle ──► Répondre capacité par capacité ──► Sauvegarder ──► Reprendre plus tard ──► Vérifier la complétude ──► Valider ──► Voir ses résultats
        (B1/B7)                     (A1 🟡)                  (B2, B3, B4 ❌)                  (B6)              (B7 🟡)                (B9 🟡)             (B9)          (D1)
```

Données : l'**évaluation** (référentiel + cible + campagne) détermine le questionnaire ; les **scores** en brouillon persistent entre les sessions ; la validation horodate et bascule l'évaluation dans les **agrégats**. Point clé : la boucle brouillon↔reprise doit être sans friction (44 capacités = plusieurs sessions de travail).

### 3. Consultation du référentiel pendant la réponse

```
Répondre à une capacité ──► Douter entre deux niveaux ──► Consulter les critères détaillés / signaux observables ──► Revenir exactement où on était
        (B2)                                                        (A3, signaux 🟡)                                       (fluidité à garantir)
```

Données : la **capacité** courante et ses **niveaux/critères** — aujourd'hui le formulaire affiche déjà les descriptions de niveaux in situ (bon réflexe à conserver), mais les signaux observables et les critères longs (`criteres-detailles.md`) ne sont pas accessibles depuis le questionnaire.

### 4. De la restitution à l'action (parcours pilote / direction)

```
Dashboard campagne ──► Repérer une entité ou une capacité faible ──► Zoomer sur l'évaluation et ses justifications ──► Comparer avec la campagne précédente ──► Exporter pour le comité ──► Plan d'action
    (D3, D4, D5)                    (D5)                                       (D1)                                        (D6, D7 ❌)                    (D10 ❌)          (D11 ❌)
```

Données : les **agrégats de campagne** → drill-down vers l'**évaluation** individuelle (scores + justifications) → mise en regard avec l'**historique** (évaluations des campagnes antérieures, même référentiel) → export.

### 5. Suivi longitudinal d'une entité (multi-référentiels)

```
Fiche entité ──► Scores par référentiel (ComNum, Design, Accessibilité, Data) ──► Évolution dans le temps sur un référentiel ──► Résultats des sites rattachés
   (D8)                        (D8)                                                       (D6)                                        (D9 🟡)
```

Données : l'**entité** agrège ses **évaluations validées** (dernière par référentiel pour l'instantané, toutes pour la courbe) et ses **sites** (chacun avec ses propres évaluations sur les référentiels « site »). Attention à la normalisation des échelles (3 vs 4 niveaux → % du max).

### 6. Ajout d'un nouveau référentiel (parcours administrateur)

```
Rédiger/importer le référentiel ──► Vérifier son rendu (dimensions, capacités, niveaux) ──► L'activer ──► Le proposer à l'évaluation ──► Versionner s'il évolue
        (E8 ❌)                                  (A2, A3)                                    (E10 ❌)              (B1)                     (E9 ❌)
```

Données : la structure complète **référentiel → dimensions → capacités → niveaux/critères** (+ cible org/site, + échelle propre). Aujourd'hui ce parcours passe par l'édition de `seed.py` et un redéploiement.

---

## Matrice tâches × rôles

Quatre rôles se dégagent de l'usage (aucun n'est outillé aujourd'hui — voir E11) :

- **Répondant** : membre d'une entité (SIRCOM ou bureau) qui remplit l'auto-évaluation.
- **Pilote de campagne** : organise les vagues d'évaluation, suit l'avancement, anime la restitution (typiquement SIRCOM / MIWEB).
- **Lecteur de résultats** : direction, comité, partie prenante — consulte sans saisir.
- **Administrateur du référentiel** : maintient les référentiels, les entités/sites et les accès.

| Tâche | Répondant | Pilote de campagne | Lecteur de résultats | Administrateur |
|---|:---:|:---:|:---:|:---:|
| **A** — Comprendre l'outil et l'échelle (A1) | ● | ● | ● | ● |
| **A** — Parcourir / chercher / filtrer le référentiel (A2–A5) | ● | ● | ○ | ● |
| **A** — Voir les moyennes par capacité (A6) | | ● | ● | |
| **B** — Démarrer une évaluation (B1) | ● | ● (pour le compte d'une entité) | | |
| **B** — Répondre, justifier, cibler les capacités applicables (B2–B4) | ● | ○ | | |
| **B** — Progresser, sauvegarder, reprendre, corriger (B5–B8) | ● | ○ | | |
| **B** — Valider l'évaluation (B9) | ● | ○ | | |
| **B** — Rouvrir une évaluation validée (B10) | ○ (la sienne) | ● | | |
| **C** — Créer / modifier / clôturer / supprimer une campagne (C1, C7–C9) | | ● | | ○ |
| **C** — Définir le périmètre, inviter, relancer (C3, C4, C6) | | ● | | |
| **C** — Suivre l'avancement (C2, C5) | ○ (sa propre échéance) | ● | ○ | |
| **D** — Voir ses propres résultats (D1) | ● | ● | ● | |
| **D** — Dashboards globaux et de campagne (D2, D3) | | ● | ● | |
| **D** — Comparer entités / campagnes, heatmap (D4, D5, D7) | | ● | ● | |
| **D** — Évolution d'une entité, synthèse multi-réf., sites (D6, D8, D9) | ○ (la sienne) | ● | ● | |
| **D** — Exporter / partager (D10) | ○ (son rapport) | ● | ● | |
| **D** — Plan d'action (D11) | ● (le sien) | ● | ○ | |
| **E** — Gérer entités et sites (E1–E6) | | ○ | | ● |
| **E** — Gérer les référentiels (E7–E10) | | ○ (consultation) | | ● |
| **E** — Gérer utilisateurs et rôles (E11) | | | | ● |

● = tâche centrale pour ce rôle · ○ = tâche occasionnelle ou en lecture seule.

**Implication UI** : le répondant n'a besoin que d'un tunnel très court (mon évaluation → répondre → valider → mes résultats) ; le pilote et le lecteur ont besoin des vues transverses ; l'administrateur des vues de gestion. La navigation actuelle (6 entrées à plat : Accueil / Référentiel / Entités / Sites / Campagnes / Évaluations) expose tout à tout le monde.

---

## Récapitulatif des tâches ❌ absentes mais nécessaires

Par ordre d'importance pour le fonctionnement réel de l'outil :

1. **C7 — Clôturer / rouvrir une campagne** : le statut existe en base mais aucune action ne le change ; toutes les campagnes restent « en cours » indéfiniment, ce qui casse la notion même de vague d'évaluation.
2. **C3 + C4 + C6 — Périmètre, invitation et relance des répondants** : sans participants attendus ni lien d'accès pré-configuré, le pilote ne peut ni mesurer la participation ni relancer, et le répondant doit reconstituer lui-même le triplet référentiel/campagne/entité (source des doublons que le code doit déjà rattraper).
3. **D10 — Exporter / partager une restitution** (rapport d'évaluation, synthèse de campagne, scores bruts en tableur) : la restitution est la finalité de l'exercice et n'est aujourd'hui possible que par capture d'écran.
4. **E8 + E9 + E10 — Administrer les référentiels** (importer, versionner, activer/désactiver) : l'ajout du référentiel Design MEF/MIWEB a nécessité de coder dans `seed.py` ; l'outil est pourtant conçu comme multi-référentiel.
5. **E2 + E5 — Modifier une entité ou un site** : seul le couple créer/supprimer existe ; corriger un nom impose de détruire l'historique d'évaluations.
6. **B4 — Adapter le questionnaire à la portée (C/D/P) / « non applicable »** : la donnée de portée existe et structure le référentiel, mais n'influence pas la passation ni le calcul des scores.
7. **E11 — Rôles et authentification** : condition transverse de « mon évaluation », des invitations et de la protection des suppressions en cascade.
