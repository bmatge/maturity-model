# Brouillon — Mini-référentiels de test

> 6 référentiels (~8-10 critères chacun) pour valider l'architecture multi-référentiel.
> Format : Dimension → Capacité → Niveaux (nombre variable selon le référentiel).
> À itérer avant intégration dans le seed.

---

## 1. Accessibilité — volet Organisation (4 niveaux)

**Cible** : organisation
**Échelle** : 4 niveaux (Émergent → Structuré → Intégré → Pérenne)

### Dimension 1 — Pilotage & engagement

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Engagement de la direction | C | La direction porte-t-elle l'accessibilité comme un objectif stratégique ? |
| 1.2 | Schéma pluriannuel | D | Existence et mise en œuvre d'un schéma pluriannuel de mise en accessibilité (obligation légale). |
| 1.3 | Budget dédié | D | Allocation de ressources financières spécifiques à l'accessibilité. |
| 1.4 | Suivi & indicateurs | D | Pilotage par indicateurs : taux de conformité, avancement du schéma, nombre de sites audités. |

**Niveaux type :**
- **1.1 — Engagement de la direction**
  1. L'accessibilité n'est pas un sujet identifié par la direction. Aucune mention dans les documents stratégiques.
  2. La direction reconnaît l'obligation légale mais ne porte pas le sujet activement. Quelques initiatives isolées.
  3. L'accessibilité est inscrite dans la feuille de route. Un·e référent·e est identifié·e. La direction arbitre en faveur de l'accessibilité.
  4. L'accessibilité est un critère de décision systématique. La direction communique sur les résultats. Le sujet est porté au plus haut niveau.

- **1.2 — Schéma pluriannuel**
  1. Pas de schéma pluriannuel publié, ou schéma obsolète non mis à jour.
  2. Schéma publié mais générique, sans actions concrètes ni calendrier précis.
  3. Schéma détaillé avec actions, calendrier, responsables identifiés. Suivi annuel effectif.
  4. Schéma intégré au pilotage global, mis à jour régulièrement, bilan publié. Aligné avec la stratégie numérique.

- **1.3 — Budget dédié**
  1. Pas de budget identifié pour l'accessibilité. Les audits et corrections sont financés au cas par cas.
  2. Budget ponctuel (un audit, une formation) mais pas de ligne récurrente.
  3. Ligne budgétaire annuelle dédiée : audits, outils, formation, correction. Suffisante pour les besoins identifiés.
  4. Budget pluriannuel sanctuarisé, révisé chaque année. Intègre la maintenance et l'amélioration continue.

- **1.4 — Suivi & indicateurs**
  1. Pas d'indicateurs de suivi. L'état de conformité des sites n'est pas connu.
  2. Suivi ponctuel : quelques taux de conformité connus mais pas consolidés. Pas de tableau de bord.
  3. Tableau de bord avec indicateurs clés (% conformité par site, avancement schéma). Suivi trimestriel.
  4. Indicateurs intégrés au reporting de la DSI/DNUM. Benchmark entre sites. Trajectoire de progression suivie.

### Dimension 2 — Compétences & culture

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Référent accessibilité | D | Existence d'un·e référent·e identifié·e avec un mandat clair. |
| 2.2 | Formation des équipes | P | Les équipes (dev, design, contenu, chef de projet) sont-elles formées ? |
| 2.3 | Intégration dans les processus | P | L'accessibilité est-elle intégrée dans le cycle de vie des projets (cahiers des charges, recette, MEP) ? |
| 2.4 | Culture & sensibilisation | P | Le sujet dépasse-t-il le cercle des experts ? L'ensemble de l'organisation est-il sensibilisé ? |

**Niveaux type :**
- **2.1 — Référent accessibilité**
  1. Pas de référent. Le sujet est porté par bonne volonté individuelle.
  2. Un·e référent·e désigné·e mais sans mandat formel ni temps dédié. Rôle consultatif.
  3. Référent·e avec mandat, temps dédié, rattachement hiérarchique clair. Reconnu·e comme point de contact.
  4. Équipe accessibilité structurée (ou réseau de référents). Expertise interne reconnue. Capacité d'accompagnement des projets.

- **2.2 — Formation des équipes**
  1. Pas de formation. Les équipes découvrent le RGAA au moment de l'audit.
  2. Quelques formations ponctuelles (sensibilisation). Pas de plan structuré.
  3. Plan de formation par profil (dev, design, rédacteurs, CP). Formations régulières. Parcours d'intégration.
  4. Culture d'apprentissage continu. Veille partagée, communauté de pratique, certifications encouragées.

- **2.3 — Intégration dans les processus**
  1. L'accessibilité est traitée en fin de projet (audit avant MEP, corrections a posteriori).
  2. L'accessibilité est mentionnée dans les cahiers des charges mais pas systématiquement vérifiée.
  3. Intégrée aux revues de conception, aux tests, à la recette. Critères d'accessibilité dans la Definition of Done.
  4. L'accessibilité est native dans tous les processus. Tests automatisés en CI. Revues de code incluent l'accessibilité.

- **2.4 — Culture & sensibilisation**
  1. Sujet perçu comme technique et contraignant. Peu de personnes concernées.
  2. Sensibilisation ponctuelle (journée mondiale, présentation interne). Intérêt croissant mais limité.
  3. Sensibilisation régulière, témoignages d'usagers, ateliers de mise en situation. Le sujet est compris au-delà des équipes techniques.
  4. L'accessibilité fait partie de la culture de l'organisation. Réflexe naturel. Portée par tous les métiers, y compris la communication.

---

## 2. Accessibilité — volet Site (3 niveaux)

**Cible** : site
**Échelle** : 3 niveaux (Insuffisant → Partiel → Conforme)

### Dimension 1 — Conformité technique

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Taux de conformité RGAA | D | Résultat du dernier audit de conformité au RGAA. |
| 1.2 | Déclaration d'accessibilité | D | Présence, complétude et mise à jour de la déclaration obligatoire. |
| 1.3 | Audit et fréquence | D | Le site fait-il l'objet d'audits réguliers et fiables ? |

**Niveaux :**
- **1.1 — Taux de conformité RGAA**
  1. Taux inconnu ou < 50%. Nombreuses non-conformités bloquantes.
  2. Taux entre 50% et 75%. Non-conformités identifiées, plan de correction en cours.
  3. Taux > 75%. Non-conformités résiduelles mineures. Dérogations documentées et justifiées.

- **1.2 — Déclaration d'accessibilité**
  1. Absente ou non conforme (pas de mention, ou simple mention "en cours").
  2. Déclaration publiée mais incomplète (manque le plan d'action, les dérogations, ou la date d'audit).
  3. Déclaration complète, à jour, conforme au modèle légal. Lien visible depuis toutes les pages.

- **1.3 — Audit et fréquence**
  1. Pas d'audit réalisé, ou audit de plus de 3 ans.
  2. Audit réalisé (externe ou auto-évaluation) mais ponctuel. Pas de suivi post-audit structuré.
  3. Audits réguliers (a minima à chaque refonte majeure). Suivi des corrections. Re-test après correction.

### Dimension 2 — Qualité de l'expérience

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Navigation & structure | D | Le site est-il navigable au clavier et avec un lecteur d'écran ? |
| 2.2 | Contenus accessibles | P | Les contenus (textes, images, documents, vidéos) sont-ils accessibles ? |
| 2.3 | Formulaires & interactions | D | Les formulaires et composants interactifs sont-ils accessibles ? |
| 2.4 | Retour utilisateur | P | Existe-t-il un canal de signalement des problèmes d'accessibilité ? |

**Niveaux :**
- **2.1 — Navigation & structure**
  1. Navigation au clavier impossible ou très dégradée. Pas de landmarks, titres de pages génériques.
  2. Navigation au clavier fonctionnelle sur les parcours principaux. Structure de titres cohérente. Quelques zones problématiques.
  3. Navigation fluide au clavier et lecteur d'écran. Landmarks, skip links, titres hiérarchisés. Parcours intégralement testés.

- **2.2 — Contenus accessibles**
  1. Images sans alternatives, documents PDF non balisés, vidéos sans sous-titres.
  2. Alternatives textuelles sur les images principales. Certains documents accessibles. Sous-titres sur les vidéos récentes.
  3. Politique systématique : toute image a une alternative, documents PDF balisés, vidéos sous-titrées et audiodécrites si pertinent.

- **2.3 — Formulaires & interactions**
  1. Formulaires sans labels associés, messages d'erreur non explicites, composants custom non accessibles.
  2. Labels présents sur la plupart des champs. Messages d'erreur identifiés. Quelques composants custom à améliorer.
  3. Tous les formulaires sont accessibles : labels, erreurs en temps réel, focus géré, composants ARIA conformes.

- **2.4 — Retour utilisateur**
  1. Pas de moyen de signaler un problème d'accessibilité (obligation légale non respectée).
  2. Adresse email de contact mentionnée dans la déclaration, mais pas de processus de traitement structuré.
  3. Canal de signalement visible, processus de traitement défini avec délais, retour systématique à l'usager.

---

## 3. Design — volet Organisation (4 niveaux)

**Cible** : organisation
**Échelle** : 4 niveaux (Émergent → Structuré → Intégré → Pérenne)
**Source** : adapté du Référentiel Maturité Design MEF (Blocs 3-4)

### Dimension 1 — Recherche utilisateur

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Exploration amont | D | L'organisation mène-t-elle des recherches avant de concevoir (benchmark, entretiens, terrain) ? |
| 1.2 | Connaissance des usagers | P | Existe-t-il des personas ou profils utilisateurs formalisés et maintenus ? |
| 1.3 | Tests utilisateurs | D | Des tests avec de vrais usagers sont-ils pratiqués ? |

**Niveaux :**
- **1.1 — Exploration amont**
  1. Pas de recherche préalable. Les projets partent d'hypothèses internes ou de demandes hiérarchiques.
  2. Benchmark ponctuel ou quelques entretiens informels. Résultats peu documentés.
  3. Recherche structurée (benchmark, entretiens métiers, observation terrain) documentée et partagée avec les parties prenantes.
  4. Recherche systématique pour tout nouveau projet. Méthodologies variées, résultats capitalisés et réutilisés.

- **1.2 — Connaissance des usagers**
  1. Pas de personas. Les publics sont décrits de manière vague ("les citoyens", "les entreprises").
  2. Personas créés pour certains projets mais non maintenus. Utilisés ponctuellement.
  3. Personas documentés, basés sur la recherche, partagés entre les équipes. Mis à jour régulièrement.
  4. Personas vivants, intégrés dans les arbitrages. Enrichis par les analytics et les retours terrain. Couvrent tous les publics.

- **1.3 — Tests utilisateurs**
  1. Aucun test avec des usagers. Les décisions se basent sur l'intuition ou le consensus interne.
  2. Tests ponctuels, souvent en fin de projet. Recommandations partiellement intégrées.
  3. Tests à chaque itération majeure, panel diversifié, recommandations systématiquement traitées.
  4. Culture du test continu. Tests intégrés au sprint. Panel récurrent d'usagers. Résultats alimentent le backlog.

### Dimension 2 — Gouvernance design

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Compétences design | D | L'organisation dispose-t-elle de compétences design (internes ou prestataires identifiés) ? |
| 2.2 | Phase d'intervention | D | À quel moment le design intervient-il dans le cycle projet ? |
| 2.3 | Processus de validation UX | P | Existe-t-il un circuit formel de validation des livrables design ? |
| 2.4 | Design system | P | L'organisation utilise-t-elle un design system partagé (DSFR ou interne) ? |

**Niveaux :**
- **2.1 — Compétences design**
  1. Aucune compétence design dans l'organisation. Le design est fait par les développeurs ou les chefs de projet.
  2. Compétence partielle (un·e CdP sensibilisé·e UX, ou designer mobilisable ponctuellement).
  3. Profil(s) design dédié(s), intégré(s) aux équipes projet. Expertise reconnue en interne.
  4. Équipe design structurée avec des rôles différenciés (UX research, UI, service design). Capacité d'accompagnement multi-projets.

- **2.2 — Phase d'intervention**
  1. Le design intervient en fin de chaîne (habillage graphique avant MEP).
  2. Le design intervient en phase de conception, mais après le cadrage fonctionnel.
  3. Le design est associé dès le cadrage. Il contribue à la définition du problème, pas seulement de la solution.
  4. Le design est natif dans la gouvernance projet. Il co-pilote avec le product management de l'idéation à la livraison.

- **2.3 — Processus de validation UX**
  1. Pas de validation UX. Les arbitrages visuels sont faits par la hiérarchie ou le client interne.
  2. Revue informelle par l'équipe projet. Pas de grille ni de rapport formalisé.
  3. Processus de validation formalisé : revue UX avec grille, rapport, suivi de la prise en compte.
  4. Validation UX intégrée au workflow projet (gate review). Critères UX dans les critères de qualité/recette.

- **2.4 — Design system**
  1. Pas de design system. Chaque projet invente ses propres composants.
  2. Le DSFR est connu mais appliqué de manière partielle ou incohérente.
  3. Le DSFR est systématiquement utilisé. Les composants custom sont documentés et partagés.
  4. Design system vivant : composants enrichis, documentation maintenue, contribution active. Gouvernance claire.

---

## 4. Design — volet Site (3 niveaux)

**Cible** : site
**Échelle** : 3 niveaux (Insuffisant → Partiel → Conforme)
**Source** : adapté du Référentiel Maturité Design MEF (Blocs 1, 5)

### Dimension 1 — Cohérence & standards

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Conformité DSFR | D | Le site applique-t-il le Design Système de l'État ? |
| 1.2 | Cohérence visuelle | P | L'interface est-elle visuellement cohérente (typographie, couleurs, espacements, composants) ? |
| 1.3 | Responsive & mobile | D | Le site est-il utilisable sur tous les écrans ? |

**Niveaux :**
- **1.1 — Conformité DSFR**
  1. DSFR non implémenté ou version obsolète. Agrément SIG non demandé.
  2. DSFR partiellement implémenté. Agrément en cours. Certaines pages ou composants non conformes.
  3. DSFR correctement implémenté, version à jour, agrément obtenu. Composants custom conformes à l'esprit DSFR.

- **1.2 — Cohérence visuelle**
  1. Incohérences visibles : mélange de styles, composants disparates, pas de grille claire.
  2. Cohérence globale respectée mais quelques écarts (pages legacy, modules tiers non stylés).
  3. Interface homogène sur l'ensemble du site. Composants réutilisés. Identité visuelle claire et constante.

- **1.3 — Responsive & mobile**
  1. Site non responsive ou très dégradé sur mobile. Navigation difficile.
  2. Responsive sur les pages principales. Quelques problèmes sur les formulaires complexes ou les tableaux.
  3. Expérience mobile soignée. Tous les parcours testés sur mobile. Performance optimisée pour les connexions lentes.

### Dimension 2 — Qualité de l'expérience utilisateur

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Clarté des parcours | P | Les parcours principaux sont-ils clairs, courts et compréhensibles ? |
| 2.2 | Qualité rédactionnelle | P | Les contenus sont-ils rédigés en langage clair et structuré ? |
| 2.3 | Performance perçue | D | Le site est-il rapide et fluide du point de vue de l'usager ? |
| 2.4 | Satisfaction usagers | P | La satisfaction des usagers est-elle mesurée et prise en compte ? |

**Niveaux :**
- **2.1 — Clarté des parcours**
  1. Parcours confus, trop d'étapes, architecture de l'information non lisible. L'usager se perd.
  2. Parcours principaux identifiés et fonctionnels. Quelques points de friction connus mais non traités.
  3. Parcours optimisés, testés avec des usagers. Arborescence claire. Aide contextuelle quand nécessaire.

- **2.2 — Qualité rédactionnelle**
  1. Jargon administratif, phrases longues, pas de structuration. Le contenu est écrit pour l'administration, pas pour l'usager.
  2. Effort de simplification sur les contenus principaux. Titres explicites. Certaines pages encore techniques.
  3. Langage clair appliqué systématiquement. Contenus structurés, testés, maintenus. Charte rédactionnelle respectée.

- **2.3 — Performance perçue**
  1. Temps de chargement > 5s, interactions lentes, impression de lourdeur.
  2. Performance correcte (< 3s) sur les pages principales. Quelques pages lentes (recherche, tableaux).
  3. Performance optimisée : Core Web Vitals au vert, chargement progressif, transitions fluides.

- **2.4 — Satisfaction usagers**
  1. Aucune mesure de satisfaction. Pas de retour usager exploité.
  2. Enquête ponctuelle ou bouton de feedback. Résultats analysés mais pas systématiquement exploités.
  3. Mesure récurrente (enquête, UX score, analytics comportemental). Résultats intégrés dans la priorisation produit.

---

## 5. Data — volet Organisation (4 niveaux)

**Cible** : organisation
**Échelle** : 4 niveaux (Émergent → Structuré → Intégré → Pérenne)

### Dimension 1 — Gouvernance data

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Stratégie data | C | L'organisation a-t-elle une stratégie data formalisée et portée par la direction ? |
| 1.2 | Rôles & responsabilités | D | Les rôles data sont-ils identifiés (CDO, DPO, référents métier, data engineers) ? |
| 1.3 | Cadre éthique & RGPD | D | L'utilisation des données respecte-t-elle un cadre éthique et réglementaire formalisé ? |

**Niveaux :**
- **1.1 — Stratégie data**
  1. Pas de stratégie data. Les données sont gérées au fil de l'eau par chaque projet.
  2. Une vision existe mais elle est informelle. Quelques initiatives data portées par des individus motivés.
  3. Stratégie data formalisée, feuille de route avec jalons, alignée sur la stratégie numérique globale.
  4. Stratégie data vivante, revue annuellement. Budget dédié. La donnée est un actif stratégique reconnu par la direction.

- **1.2 — Rôles & responsabilités**
  1. Pas de rôle data identifié. La gestion des données incombe aux développeurs projet par projet.
  2. Un DPO existe (obligation légale). Quelques profils data mais sans coordination.
  3. Organisation data structurée : CDO ou équivalent, référents métier, data engineers. Responsabilités claires.
  4. Communauté data active. Réseau de référents dans les directions. Montée en compétence organisée. Filière data reconnue.

- **1.3 — Cadre éthique & RGPD**
  1. Conformité RGPD minimale (registre de traitement). Pas de réflexion éthique sur l'usage des données.
  2. RGPD respecté formellement. Sensibilisation des équipes. Pas de cadre éthique au-delà du réglementaire.
  3. Cadre éthique formalisé pour l'usage des données (IA, profilage, open data). PIA systématiques sur les projets sensibles.
  4. Éthique data intégrée dans la culture. Comité éthique ou processus de revue. Transparence sur les algorithmes publics.

### Dimension 2 — Compétences & culture data

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Littératie data | P | Les agents comprennent-ils les données qu'ils manipulent et savent-ils les interpréter ? |
| 2.2 | Outillage & accès | D | Les équipes disposent-elles d'outils adaptés pour accéder aux données et les exploiter ? |
| 2.3 | Partage & documentation | P | Les jeux de données internes sont-ils documentés, catalogués et partagés ? |

**Niveaux :**
- **2.1 — Littératie data**
  1. Les données sont manipulées sans compréhension (copier-coller de tableaux, pas d'esprit critique sur les chiffres).
  2. Quelques agents formés (Excel avancé, notions de dataviz). La majorité consomme des données sans les questionner.
  3. Formation data intégrée aux parcours métier. Les agents savent lire un dashboard, poser des questions aux données.
  4. Culture data-driven. Les décisions s'appuient sur les données. Les agents sont autonomes dans l'exploration de données.

- **2.2 — Outillage & accès**
  1. Pas d'outil de datavisualisation ou de requêtage accessible aux métiers. Tout passe par la DSI.
  2. Quelques outils disponibles (Excel, BI ponctuel) mais pas d'accès self-service aux données.
  3. Plateforme data accessible aux métiers. Dashboards partagés. Catalogue de données consultable.
  4. Data platform mature : accès self-service, API internes, documentation automatisée, monitoring qualité.

- **2.3 — Partage & documentation**
  1. Données en silos. Chaque direction a ses propres fichiers, pas de vision transverse.
  2. Quelques jeux de données partagés de manière informelle. Pas de catalogue ni de documentation standardisée.
  3. Catalogue de données interne. Métadonnées documentées. Responsables identifiés par jeu de données.
  4. Données internes accessibles et documentées par défaut. Politique d'open data interne. Processus de mise à jour automatisé.

---

## 6. Data — volet Site (3 niveaux)

**Cible** : site
**Échelle** : 3 niveaux (Insuffisant → Partiel → Conforme)

### Dimension 1 — Mesure & analytics

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 1.1 | Outil de mesure | D | Le site dispose-t-il d'un outil de mesure d'audience respectueux du RGPD ? |
| 1.2 | Qualité du suivi | D | Les indicateurs clés sont-ils définis et suivis ? |
| 1.3 | Exploitation des données | P | Les données analytics sont-elles exploitées pour améliorer le site ? |

**Niveaux :**
- **1.1 — Outil de mesure**
  1. Pas d'outil de mesure, ou outil non conforme RGPD (Google Analytics sans consentement).
  2. Outil en place (Matomo, AT Internet…) mais configuration partielle (pas de suivi des événements, pas de goals).
  3. Outil conforme RGPD correctement configuré. Suivi des pages, événements, conversions. Données fiables et complètes.

- **1.2 — Qualité du suivi**
  1. Pas d'indicateurs définis. Les données brutes existent mais personne ne les regarde.
  2. Quelques KPIs suivis (pages vues, visiteurs) mais pas de tableau de bord ni de revue régulière.
  3. KPIs définis par objectif du site. Tableau de bord partagé avec l'équipe. Revue mensuelle ou bimensuelle.

- **1.3 — Exploitation des données**
  1. Les données ne sont pas exploitées. Pas de lien entre analytics et décisions produit.
  2. Analyse ponctuelle pour justifier des évolutions ou répondre à des questions. Pas de démarche proactive.
  3. Démarche data-driven : les analytics alimentent le backlog, valident les hypothèses, mesurent l'impact des évolutions.

### Dimension 2 — Transparence & ouverture

| # | Capacité | Portée | Description |
|---|----------|--------|-------------|
| 2.1 | Conformité cookies & traceurs | D | La gestion des cookies est-elle conforme au RGPD et à la recommandation CNIL ? |
| 2.2 | Open data | P | Le site contribue-t-il à l'ouverture des données publiques ? |
| 2.3 | API & interopérabilité | D | Le site expose-t-il des données via des API documentées ? |

**Niveaux :**
- **2.1 — Conformité cookies & traceurs**
  1. Pas de bandeau cookies, ou consentement non recueilli correctement. Traceurs tiers non maîtrisés.
  2. Bandeau cookies présent mais configuration imparfaite (refus pas aussi simple qu'acceptation, traceurs avant consentement).
  3. Gestion des cookies conforme : consentement libre, refus aussi simple qu'acceptation, pas de traceur avant choix, revue périodique.

- **2.2 — Open data**
  1. Pas de données ouvertes. Le site ne publie ni ne référence de jeux de données.
  2. Quelques jeux de données publiés sur data.gouv.fr mais pas maintenus ou mal documentés.
  3. Politique d'ouverture : jeux de données identifiés, publiés, documentés, mis à jour. Référencés sur data.gouv.fr.

- **2.3 — API & interopérabilité**
  1. Pas d'API. Les données du site ne sont accessibles qu'en naviguant sur les pages.
  2. API existante mais non documentée ou non maintenue. Usage interne uniquement.
  3. API documentée (OpenAPI/Swagger), versionnée, monitorée. Utilisée par des tiers. Référencée sur api.gouv.fr.
