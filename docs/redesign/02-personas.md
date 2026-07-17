# Personas — Refonte UI de l'outil de maturité

> **Socle de la refonte.** Ces personas sont déduits de ce que l'application permet réellement
> (routes Flask, modèle de données, templates) et du contexte métier des référentiels
> (`referentiel-v2.md`, `criteres-detailles.md`, référentiels Design MEF/MIWEB seedés).
> Ils ne décrivent pas des profils démographiques mais des **rapports distincts à l'outil**.

## Ce que le code permet — rappel factuel

L'application n'a ni authentification ni rôles : les personas correspondent aux **trois parcours
implicites** que le code dessine.

| Parcours dans le code | Routes / écrans concernés |
|---|---|
| **Répondre à une évaluation** | `evaluation_new` (choix référentiel + entité/site + campagne, champ `evaluateur` libre), `evaluation_fill` (une note 1→3 ou 1→4 par capacité + justification, brouillon/validation, barre de progression), `evaluation_results` (radar, détail par capacité) |
| **Piloter le dispositif** | `campagne_new`/`campagnes_list`, `entite_new`/`site_new` (+ suppressions), `evaluations_list`, `campagne_dashboard` (moyennes, écart-type, radar comparatif, heatmap entité × capacité), `referentiel_view` (consultation des critères + moyennes par capacité) |
| **Consulter la restitution** | `index` (KPIs, radar global, bar chart par entité), `entite_evolution` (courbes dans le temps, par référentiel), `evaluation_results`, `campagne_dashboard` |

Le **référentiel lui-même n'est pas administrable dans l'UI** (création/édition uniquement via
`seed.py`) : « l'administrateur du référentiel » n'est donc pas un persona de l'interface, mais un
rôle de mainteneur du code, confondu en pratique avec le persona 2.

---

## Persona 1 — Camille, répondante d'évaluation
**Référente design / com numérique d'une direction (bureau de communication, équipe produit)**

### Contexte de travail
Camille travaille dans un bureau de communication ou une équipe numérique d'une direction du
ministère (type « Bureau com — Santé » du seed). Elle est agent public, à l'aise avec les outils
web du quotidien mais **elle n'a pas conçu le référentiel** : elle le découvre au moment où on lui
demande d'évaluer son entité (référentiel organisation) ou l'un de ses sites (référentiel site).
Elle connaît bien, en revanche, la réalité de terrain qu'elle doit noter : ses pratiques design,
ses contenus, ses outils.

### Objectifs vis-à-vis de l'app
1. **Répondre à la campagne** qu'on lui a demandé de compléter, dans un temps raisonnable, sans se tromper de référentiel ni de cible.
2. **Comprendre chaque capacité et chaque niveau** assez vite pour se positionner honnêtement (les critères 1→4 sont longs et nuancés : « Émergent » vs « Structuré » demande une vraie lecture).
3. **S'auto-situer sans se sur- ou sous-noter** : les descriptions de niveaux servent de garde-fou, les justifications lui permettent d'assumer sa note.
4. **Interrompre et reprendre** la saisie (le brouillon existe pour ça : 44 capacités pour ComNum, 15 pour Design-org, ça ne se fait pas d'une traite).
5. **Voir immédiatement son résultat** (radar, points forts/faibles) pour que l'exercice lui rapporte quelque chose à elle, pas seulement au niveau central.

### Valeur retirée
Par rapport à un tableur envoyé par mail : les **critères détaillés de chaque niveau sont sous ses
yeux au moment de noter** (pas dans un PDF annexe), la progression est visible, le brouillon évite
de perdre sa saisie, et surtout elle obtient une **restitution instantanée et lisible** de sa
propre entité — un radar qu'elle peut montrer à son chef de bureau, au lieu d'une ligne dans un
fichier consolidé qu'elle ne reverra jamais.

### Fréquence & mode d'usage
**Ponctuel et espacé** : une à deux fois par an, au rythme des campagnes, plus éventuellement une
évaluation « hors campagne » d'un site. Chaque usage est une **session longue** (30–60 min,
possiblement fractionnée), suivie d'une consultation courte des résultats. Entre deux campagnes,
elle n'ouvre pas l'outil — chaque retour est une **re-découverte**.

### Frustrations potentielles / risques d'abandon
- **Longueur du questionnaire** : 44 capacités × 4 niveaux à lire = fatigue, risque de notation de plus en plus expéditive vers la fin (biais sur les dernières dimensions).
- **Jargon du référentiel** : « portée C/D/P », « capacité », « dette éditoriale », « design system » — vocabulaire d'experts qui peut la faire douter de sa légitimité à répondre.
- **Peur de la note** : l'exercice ressemble à un contrôle ; si elle sent que sa note remonte « en central » sans contexte, elle lisse ses réponses ou délègue.
- **Doute entre deux niveaux** : quand sa réalité est entre « Structuré » et « Intégré », l'absence de demi-mesure la bloque ; la justification est sa soupape, encore faut-il qu'elle comprenne à quoi elle sert.
- **Interruption non pardonnée** : si elle perd 30 minutes de saisie, elle ne revient pas.

### Niveau d'expertise design & data
**Design : intermédiaire hétérogène** (certaines répondantes sont designers, d'autres chargées de
com sans culture design) — le vocabulaire de l'UI doit être compréhensible sans le glossaire.
**Data : faible à moyenne** — un radar et des libellés de niveaux lui parlent ; un écart-type, non.

---

## Persona 2 — Nadia, pilote du dispositif d'évaluation
**Cheffe de projet maturité au niveau central (SIRCOM / mission MIWEB), co-autrice du référentiel**

### Contexte de travail
Nadia est au service central (type SIRCOM ou mission web ministérielle). Elle a **participé à la
conception du référentiel** — elle en maîtrise la structure (dimensions, capacités, portées,
niveaux) et son intention (mesurer la pérennité des pratiques, pas la performance). C'est elle qui
fait vivre le dispositif : c'est l'utilisatrice qui exerce toutes les fonctions d'administration
que l'UI expose (créer campagnes, entités, sites ; supprimer ; suivre). Quand le référentiel doit
évoluer, c'est elle (ou son binôme dev) qui touche au seed — hors UI.

### Objectifs vis-à-vis de l'app
1. **Lancer une campagne** : la créer, préparer la liste des entités/sites à évaluer, s'assurer que chaque répondant évalue la bonne cible avec le bon référentiel.
2. **Suivre l'avancement** : distinguer brouillons et évaluations validées, relancer les entités manquantes avant la clôture.
3. **Analyser les résultats agrégés** : moyennes et dispersions par dimension, heatmap entité × capacité pour repérer les capacités faibles partout (chantier transverse) vs les entités faibles partout (accompagnement ciblé).
4. **Comparer dans le temps** : mesurer si les entités progressent d'une campagne à l'autre — c'est la preuve d'impact de son dispositif.
5. **Garantir la qualité des données** : détecter les évaluations aberrantes ou expéditives (via les justifications), nettoyer les doublons, gérer le cycle de vie des campagnes.

### Valeur retirée
Par rapport à Excel : la **collecte est distribuée** (chaque entité saisit elle-même, pas de
consolidation manuelle de 15 fichiers), les **agrégats sont calculés automatiquement** (moyennes,
écarts-types, heatmap) et **l'historique est structuré** (une évaluation = une entité × un
référentiel × une campagne, comparable dans le temps). L'outil transforme une corvée de
consolidation trimestrielle en un tableau de bord permanent, et rend le multi-référentiel
(ComNum, Design, Accessibilité) tenable — chose ingérable en tableur.

### Fréquence & mode d'usage
**Récurrent et intensif par vagues** : usage quasi quotidien pendant une campagne (préparation,
suivi, relances, analyse), puis usage d'analyse et de restitution entre les campagnes (préparer
des comités, comparer les trajectoires). C'est la seule utilisatrice qui connaît **tous** les
écrans de l'application.

### Frustrations potentielles / risques d'abandon
- **Pas de vue d'avancement synthétique** par nature de la tâche : suivre « qui a répondu, qui est en brouillon, qui n'a rien commencé » sur N entités × M référentiels est son stress principal en période de campagne.
- **Risque d'erreur destructive** : elle manipule des suppressions en cascade (entité → évaluations → scores) ; une fausse manœuvre détruit de l'historique irremplaçable.
- **Restitution à retravailler** : si elle doit refaire les graphiques dans PowerPoint pour son comité, l'outil perd la moitié de sa valeur.
- **Rigidité du référentiel** : toute évolution des critères passe par le code ; si le dispositif vit, cette friction s'accumule sur elle.
- **Comparabilité fragile** : entités qui sautent une campagne, référentiels qui changent de version — ses séries temporelles se trouent vite et l'analyse devient contestable.

### Niveau d'expertise design & data
**Design : experte** — c'est son référentiel, le jargon ne la gêne pas. **Data : bonne** —
moyennes, dispersions, heatmaps sont son langage de travail ; elle veut de la densité
d'information, pas de la vulgarisation.

---

## Persona 3 — Marc, sponsor de la démarche
**Manager / décideur (chef du SIRCOM, sous-directeur, sponsor de la transformation)**

### Contexte de travail
Marc dirige le service qui porte la démarche, ou finance/arbitre la transformation numérique et
design. Il **ne saisit jamais rien** : il consomme la restitution — le dashboard d'accueil, le
dashboard de campagne, l'évolution d'une entité — souvent en réunion, parfois via une capture
dans un support. Il connaît la démarche dans ses grandes lignes mais pas le détail des 44
capacités ; sa familiarité avec le référentiel se limite aux noms des dimensions.

### Objectifs vis-à-vis de l'app
1. **Voir l'état de maturité en un coup d'œil** : où en est-on globalement, quelles dimensions sont faibles, quelles entités décrochent.
2. **Arbitrer** : décider où mettre les moyens (formation, recrutement, chantier design system) sur la base des écarts constatés — la heatmap et les comparaisons entité par entité sont ses arguments.
3. **Prouver la progression** : montrer à sa hiérarchie ou aux cabinets que la démarche produit des effets d'une campagne à l'autre (courbes d'évolution).
4. **Objectiver les demandes** des entités : quand un bureau réclame des moyens, situer sa demande par rapport à son niveau mesuré.

### Valeur retirée
Par rapport à un rapport annuel ou un slide consolidé à la main : une **image à jour, homogène et
comparable** de toutes les entités sur une grille unique — la légitimité de l'outil (référentiel
partagé, auto-évaluation tracée avec justifications) rend les écarts **discutables mais pas
contestables**. C'est un instrument d'objectivation des arbitrages, pas un outil de travail.

### Fréquence & mode d'usage
**Épisodique et bref** : quelques minutes à la clôture d'une campagne, avant un comité ou un
arbitrage budgétaire. Souvent en présence de Nadia qui commente. Il ne descend presque jamais
sous le niveau « dimension » ; quand il le fait, c'est pour une entité précise qui pose question.

### Frustrations potentielles / risques d'abandon
- **Surcharge d'information** : radars multi-séries, écarts-types, heatmap de 44 colonnes — s'il doit demander à Nadia de « traduire », l'outil ne lui sert à rien en direct.
- **Absence de hiérarchie du message** : il cherche « les 3 choses à retenir », pas l'exhaustivité ; une restitution qui ne priorise pas le laisse indifférent.
- **Score sans signification actionnable** : « 2,4/4 » ne déclenche rien s'il ne sait pas si c'est bien, en progrès, ou alarmant — il lui faut des repères (seuils, tendance, comparaison).
- **Défiance sur la donnée** : de l'auto-déclaratif ; s'il soupçonne de la complaisance, il disqualifie tout l'exercice. La visibilité des justifications et du taux de participation est son gage de confiance.

### Niveau d'expertise design & data
**Design : faible** — les noms de dimensions doivent parler d'eux-mêmes. **Data : moyenne mais
pressée** — il lit un graphique simple, une tendance, un code couleur ; pas un écart-type ni un
radar à six séries superposées.

---

## Persona prioritaire

**Camille (la répondante) prime dans les arbitrages UX.**

Trois raisons :

1. **Toute la chaîne de valeur dépend d'elle.** Sans réponses complètes, honnêtes et menées au
   bout, les dashboards de Nadia sont vides et les arbitrages de Marc sans fondement. Le maillon
   faible du dispositif est le taux de complétion et la sincérité de l'auto-évaluation — deux
   variables directement gouvernées par l'expérience du questionnaire (longueur perçue, clarté
   des critères, sentiment de sécurité, récompense immédiate par la restitution).
2. **C'est le persona le plus nombreux et le moins captif.** Nadia utilisera l'outil quoi qu'il
   arrive (c'est son dispositif) ; Marc est accompagné quand il le consulte. Camille est seule
   face à l'écran, une à deux fois par an, sans mémoire de l'outil : chaque défaut d'ergonomie se
   paie en abandon ou en données bâclées.
3. **Ses contraintes tirent tout le monde vers le haut.** Un questionnaire séquencé, un
   vocabulaire désambiguïsé, une restitution lisible sans expertise data servent aussi la qualité
   des données de Nadia et la lisibilité des synthèses de Marc — l'inverse n'est pas vrai.

**Ordre d'arbitrage en cas de conflit UX : Camille > Nadia > Marc.** Nadia reste le second
prioritaire car elle est la seule utilisatrice quotidienne et l'administratrice de fait : ses
besoins (suivi d'avancement, sécurité des suppressions, densité analytique) structurent les écrans
que Camille ne voit jamais.
