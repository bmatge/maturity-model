"""
Seed du référentiel v2 — 44 capacités × 4 niveaux = 176 critères.
Exécuté automatiquement au premier lancement si la DB est vide.
"""

from models import (
    db, ReferentielVersion, Dimension, Capacite, NiveauCritere, Entite, Campagne, Site
)
from datetime import date

NOMS_NIVEAUX = {1: "Émergent", 2: "Structuré", 3: "Intégré", 4: "Pérenne"}

# ──────────────────────────────────────────────
# Données du référentiel v2
# ──────────────────────────────────────────────

DIMENSIONS = [
    {
        "numero": 1,
        "nom": "Vision & positionnement",
        "description": "Le pourquoi : quel rôle joue la communication numérique dans la mission du ministère ?",
        "capacites": [
            {
                "numero": "1.1", "nom": "Vision stratégique", "portee": "C",
                "description": "Existence, horizon et formalisation d'une vision pour la communication numérique.",
                "niveaux": [
                    "Pas de vision formalisée. La communication numérique se gère au jour le jour, en réaction aux demandes.",
                    "Une vision existe mais elle est informelle, portée par quelques personnes clés. Elle est exprimée oralement mais pas documentée.",
                    "Vision formalisée dans un document de référence, avec un horizon de 3 à 5 ans. Déclinée en feuille de route opérationnelle avec des jalons.",
                    "La vision est régulièrement actualisée (revue annuelle a minima). Elle s'intègre dans les documents stratégiques du ministère. Sa mise à jour est un processus.",
                ]
            },
            {
                "numero": "1.2", "nom": "Partage de la vision", "portee": "P",
                "description": "Diffusion de la vision auprès des équipes, des directions et des cabinets.",
                "niveaux": [
                    "La vision reste dans la tête de quelques personnes. Les bureaux de communication des directions ne la connaissent pas.",
                    "La vision est partagée ponctuellement, de manière informelle — lors de réunions, par email. Connue du cercle rapproché.",
                    "La vision est partagée de manière formelle et régulière : comités éditoriaux, présentations aux directions, documents accessibles.",
                    "La vision irrigue l'ensemble de l'organisation. Les bureaux la déclinent dans leur contexte. Elle fait partie de la culture partagée.",
                ]
            },
            {
                "numero": "1.3", "nom": "Positionnement éditorial", "portee": "P",
                "description": "Clarté sur ce que la communication numérique apporte : information, service, engagement, transparence.",
                "niveaux": [
                    "La communication numérique est un relais d'information institutionnelle. On publie ce qu'on nous demande, sans réflexion sur la valeur apportée.",
                    "Le positionnement est identifié mais pas formalisé. Il dépend de la sensibilité des personnes en poste.",
                    "Positionnement éditorial clairement formalisé, décliné par canal et par public. Il guide les choix de contenu.",
                    "Le positionnement est régulièrement questionné et ajusté en fonction des usages constatés et des retours des publics.",
                ]
            },
            {
                "numero": "1.4", "nom": "Articulation com globale", "portee": "C",
                "description": "Intégration de la stratégie numérique dans la stratégie de communication globale du ministère.",
                "niveaux": [
                    "La communication numérique fonctionne en silo. Perçue comme un canal technique, pas une composante stratégique.",
                    "Des échanges réguliers existent entre équipes numériques et communication traditionnelle. Le numérique est associé aux campagnes majeures.",
                    "La stratégie numérique est intégrée dans la stratégie de communication globale. Les plans incluent le volet numérique dès la conception.",
                    "Communication numérique et traditionnelle sont pensées comme un tout. Le numérique est une dimension native de toute action de communication.",
                ]
            },
            {
                "numero": "1.5", "nom": "Coordination multi-entités", "portee": "P",
                "description": "Mécanismes de coordination entre SIRCOM et bureaux de communication des directions.",
                "niveaux": [
                    "Chaque entité communique de manière autonome, sans coordination. Des incohérences de message ou de calendrier sont fréquentes.",
                    "Des échanges informels existent. Le SIRCOM donne des directives ponctuelles. La coordination dépend des relations interpersonnelles.",
                    "Instances de coordination formelles : comités éditoriaux réguliers, chartes partagées, calendrier éditorial commun.",
                    "Écosystème coordonné avec autonomie encadrée. Les bonnes pratiques circulent. Le système fonctionne même quand les personnes changent.",
                ]
            },
        ]
    },
    {
        "numero": 2,
        "nom": "Connaissance des publics",
        "description": "La base des décisions : qui sont nos publics, que font-ils, qu'attendent-ils ?",
        "capacites": [
            {
                "numero": "2.1", "nom": "Identification des publics", "portee": "P",
                "description": "Segmentation et caractérisation des audiences cibles.",
                "niveaux": [
                    "Les publics ne sont pas segmentés. On communique « au grand public » sans distinction.",
                    "Les principales audiences sont identifiées mais pas caractérisées en profondeur. La segmentation reste intuitive.",
                    "Personas ou segments formalisés avec des besoins documentés. La segmentation guide les choix éditoriaux.",
                    "Segmentation vivante, actualisée régulièrement à partir des données d'usage et de la recherche utilisateur.",
                ]
            },
            {
                "numero": "2.2", "nom": "Recherche utilisateur", "portee": "P",
                "description": "Méthodes et fréquence des études qualitatives et quantitatives sur les besoins des usagers.",
                "niveaux": [
                    "Pas de recherche utilisateur. Les décisions éditoriales sont prises sur la base de l'intuition ou des demandes internes.",
                    "Études ou tests ponctuels, généralement liés à un projet de refonte. Les résultats ne sont pas capitalisés.",
                    "Recherche utilisateur régulière et méthodique : entretiens, tests d'utilisabilité, enquêtes. Les résultats alimentent les décisions.",
                    "Dispositif continu de recherche intégré aux processus de conception et d'évolution. Panel d'utilisateurs mobilisable.",
                ]
            },
            {
                "numero": "2.3", "nom": "Analyse des usages", "portee": "D",
                "description": "Exploitation des données d'audience et de comportement sur les canaux numériques.",
                "niveaux": [
                    "Pas de suivi d'audience, ou données collectées mais non exploitées.",
                    "Statistiques d'audience consultées ponctuellement. L'analyse reste descriptive et rétrospective.",
                    "Tableaux de bord structurés avec des indicateurs définis par canal. Analyse régulière des parcours et contenus performants.",
                    "Données d'usage croisées entre canaux, exploitées en continu pour orienter les décisions éditoriales. Culture de la donnée installée.",
                ]
            },
            {
                "numero": "2.4", "nom": "Écoute et feedback", "portee": "P",
                "description": "Dispositifs de recueil des retours citoyens.",
                "niveaux": [
                    "Pas de dispositif structuré de recueil des retours. Les remontées arrivent par email ou téléphone, traitées au cas par cas.",
                    "Formulaires de contact ou enquêtes occasionnelles. Les retours sont lus mais pas analysés systématiquement.",
                    "Dispositifs structurés : enquêtes de satisfaction régulières, boutons de feedback, analyse des commentaires réseaux sociaux.",
                    "Boucle de feedback complète : recueil → analyse → action → communication des améliorations. Les usagers voient leurs retours pris en compte.",
                ]
            },
            {
                "numero": "2.5", "nom": "Veille et e-réputation", "portee": "C",
                "description": "Suivi de ce qui se dit du ministère et de ses politiques publiques en ligne.",
                "niveaux": [
                    "Pas de veille structurée. On découvre les sujets polémiques quand ils remontent via la presse ou le cabinet.",
                    "Veille informelle portée par quelques personnes (alertes Google, lecture de presse). Partage oral en cas de sujet sensible.",
                    "Veille outillée et régulière. Rapports partagés. Alertes automatisées en cas de pic ou de crise.",
                    "Veille intégrée au pilotage de la communication : elle alimente la stratégie éditoriale, la communication de crise et le positionnement.",
                ]
            },
        ]
    },
    {
        "numero": 3,
        "nom": "Design & cohérence",
        "description": "L'identité et l'expérience : comment on se présente et comment on est perçu.",
        "capacites": [
            {
                "numero": "3.1", "nom": "Design system", "portee": "C",
                "description": "Existence et adoption d'un système de design vivant et partagé, intégrant le DSFR.",
                "niveaux": [
                    "Pas de design system. Chaque projet définit ses propres composants visuels. Le DSFR est connu mais pas appliqué.",
                    "Charte graphique existante (souvent un PDF). Le DSFR est appliqué sur les nouveaux projets. Composants pas partagés de manière vivante.",
                    "Design system vivant, maintenu et partagé. Le DSFR est intégré comme socle. Composants réutilisables, documentés, versionnés.",
                    "Design system en amélioration continue, alimenté par les retours des équipes. Contributions ouvertes. Documentation toujours à jour.",
                ]
            },
            {
                "numero": "3.2", "nom": "Charte éditoriale", "portee": "P",
                "description": "Règles d'écriture, tonalité, langage clair, adaptées aux canaux et aux publics.",
                "niveaux": [
                    "Pas de charte éditoriale. Chacun écrit selon ses habitudes. Le ton et les formats varient d'un rédacteur à l'autre.",
                    "Des recommandations existent mais elles sont peu connues ou peu suivies. La qualité dépend des compétences individuelles.",
                    "Charte éditoriale formalisée, accessible, appliquée. Elle couvre le ton, le langage clair, les formats par canal.",
                    "Charte vivante, actualisée régulièrement. Formation des nouveaux arrivants. Relecture systématique au regard de la charte.",
                ]
            },
            {
                "numero": "3.3", "nom": "Expérience utilisateur", "portee": "P",
                "description": "Prise en compte de l'UX dans la conception des parcours et des interfaces.",
                "niveaux": [
                    "L'UX n'est pas un sujet identifié. Les interfaces sont conçues sans méthodologie spécifique.",
                    "Sensibilisation à l'UX. Quelques bonnes pratiques appliquées ponctuellement. Pas de compétence dédiée.",
                    "Démarche UX systématique : recherche, wireframes, prototypes, tests. Compétences dédiées. L'UX est intégrée au cycle projet.",
                    "Design centré utilisateur comme pratique par défaut. L'UX est une posture permanente. Parcours optimisés en continu.",
                ]
            },
            {
                "numero": "3.4", "nom": "Accessibilité", "portee": "P",
                "description": "Conformité RGAA et intégration de l'accessibilité dans le processus de design.",
                "niveaux": [
                    "L'accessibilité est connue (obligation légale) mais peu avancée. Conformité RGAA < 50 %. Schéma pluriannuel formel mais pas suivi.",
                    "Audits réalisés. Conformité 50-75 %. Améliorations correctives engagées. Déclaration d'accessibilité publiée.",
                    "Accessibilité intégrée dès la conception. Réduction active de la dette. Conformité 75-90 %. Formation des contributeurs.",
                    "Évaluation et amélioration continues. Conformité visée 100 %. Accessibilité perçue comme un standard de qualité. Audits réguliers.",
                ]
            },
            {
                "numero": "3.5", "nom": "Cohérence multicanale", "portee": "C",
                "description": "Homogénéité de l'identité, du ton et de l'expérience à travers tous les canaux.",
                "niveaux": [
                    "Chaque canal a sa propre identité. Un citoyen perçoit des communications disparates d'un canal à l'autre.",
                    "Cohérence visuelle assurée (logo, couleurs) mais pas éditoriale. Le ton varie fortement entre canaux.",
                    "Identité, ton et expérience harmonisés sur l'ensemble des canaux. La charte éditoriale est déclinée par canal.",
                    "Expérience cohérente et adaptée : chaque canal exploite ses spécificités tout en maintenant l'unité. Passerelles actives entre canaux.",
                ]
            },
            {
                "numero": "3.6", "nom": "Éco-conception", "portee": "P",
                "description": "Prise en compte de l'impact environnemental dans les choix de design et de développement.",
                "niveaux": [
                    "L'éco-conception n'est pas prise en compte. Le poids des pages et la sobriété ne sont pas des critères.",
                    "Sensibilisation en cours. Quelques bonnes pratiques (optimisation images, limitation vidéos autoplay). Pas de démarche structurée.",
                    "Éco-conception intégrée dans les cahiers des charges. Mesure de l'impact (RGESN, poids des pages). Arbitrages documentés.",
                    "Démarche systématique. Évaluation régulière et amélioration continue. Budget carbone numérique suivi. La sobriété est un réflexe partagé.",
                ]
            },
        ]
    },
    {
        "numero": 4,
        "nom": "Écosystème éditorial",
        "description": "Les canaux et leur articulation : où et comment on communique.",
        "capacites": [
            {
                "numero": "4.1", "nom": "Sites web et services en ligne", "portee": "P",
                "description": "Gestion du parc de sites, qualité, évolution continue vs refontes.",
                "niveaux": [
                    "Parc de sites non maîtrisé. Chaque direction gère les siens. Refontes récurrentes et coûteuses.",
                    "Parc identifié et cartographié. Rationalisation en cours. Logique « projet » plutôt que « produit ».",
                    "Évolution continue avec une logique de service. Qualité mesurée (Observatoire, analytics). Priorisation basée sur les usages.",
                    "Parc piloté comme un portefeuille de produits numériques. Évolution continue basée sur les données d'usage. Rationalisation permanente.",
                ]
            },
            {
                "numero": "4.2", "nom": "Réseaux sociaux", "portee": "P",
                "description": "Stratégie de présence, ligne éditoriale par plateforme, community management.",
                "niveaux": [
                    "Présence non structurée. Publications au fil de l'eau, sans ligne éditoriale. Pas de community management actif.",
                    "Comptes identifiés et rationalisés. Ligne éditoriale sommaire. Publication planifiée. Modération réactive.",
                    "Stratégie par plateforme avec ligne éditoriale formalisée. Community management actif. Mesure des performances.",
                    "Stratégie intégrée à la communication globale. Expérimentation de nouveaux formats. Adaptation continue aux plateformes.",
                ]
            },
            {
                "numero": "4.3", "nom": "Email et newsletters", "portee": "P",
                "description": "Stratégie de diffusion directe, segmentation, gestion des bases d'abonnés.",
                "niveaux": [
                    "Pas de newsletter ou envois ponctuels sans stratégie. Bases d'abonnés non gérées.",
                    "Newsletter existante avec envois réguliers. Base gérée (inscription/désinscription). Contenus pas segmentés.",
                    "Stratégie de diffusion définie. Segmentation par audience. Mesure des performances. Templates conformes.",
                    "Communications personnalisées. Base segmentée et qualifiée en continu. Tests A/B. Intégration CRM.",
                ]
            },
            {
                "numero": "4.4", "nom": "Vidéo et multimédia", "portee": "P",
                "description": "Capacité de production, chaîne éditoriale audiovisuelle, diffusion.",
                "niveaux": [
                    "Production vidéo rare ou inexistante. Sous-traitée intégralement sans capitalisation.",
                    "Production ponctuelle pour événements ou campagnes majeures. Formats standards (interview, captation).",
                    "Chaîne de production structurée avec des formats définis. Sous-titrage et audiodescription systématiques.",
                    "Production intégrée à la stratégie éditoriale. Formats adaptés par canal et public. Compétences internes suffisantes.",
                ]
            },
            {
                "numero": "4.5", "nom": "Relations presse numériques", "portee": "C",
                "description": "Newsroom, dossiers de presse, communiqués, espace presse en ligne.",
                "niveaux": [
                    "Communiqués envoyés par email. Pas d'espace presse en ligne ou espace obsolète.",
                    "Espace presse basique sur le site web. Communiqués et dossiers au format PDF. Mise à jour irrégulière.",
                    "Newsroom structurée : communiqués, dossiers, visuels et vidéos téléchargeables. Contenus multimédias adaptés.",
                    "Newsroom dynamique intégrée au site principal. Flux d'information en temps réel. Analytics de consultation.",
                ]
            },
            {
                "numero": "4.6", "nom": "Communication de crise", "portee": "C",
                "description": "Protocoles numériques de communication de crise, réactivité, coordination.",
                "niveaux": [
                    "Pas de protocole numérique de crise. Réaction au cas par cas. Canaux numériques sous-exploités.",
                    "Protocole basique : liste de contacts d'urgence, process d'alerte. Activé ponctuellement mais pas testé.",
                    "Protocole formalisé et testé. Coordination claire entre SIRCOM, bureaux et cabinets. Templates prêts à l'emploi.",
                    "Dispositif testé régulièrement (exercices de simulation). Retex systématiques. Protocole mis à jour en conséquence.",
                ]
            },
            {
                "numero": "4.7", "nom": "Communication interne", "portee": "P",
                "description": "Intranet, outils collaboratifs, diffusion interne d'information.",
                "niveaux": [
                    "Communication interne limitée aux emails et un intranet statique. L'information circule mal.",
                    "Intranet actif et mis à jour. Quelques outils collaboratifs déployés. Efforts de diffusion mais audience limitée.",
                    "Écosystème interne structuré : intranet éditorialisé, réseau social d'entreprise, newsletter interne, outils collaboratifs.",
                    "Communication interne et externe alignées. Agents ambassadeurs sur les réseaux sociaux. L'information descend et remonte.",
                ]
            },
        ]
    },
    {
        "numero": 5,
        "nom": "Corpus & patrimoine éditorial",
        "description": "Les briques durables : les contenus structurés qui constituent le patrimoine informationnel.",
        "capacites": [
            {
                "numero": "5.1", "nom": "Structuration des contenus", "portee": "P",
                "description": "Modèles de contenu, taxonomies, métadonnées, typologies.",
                "niveaux": [
                    "Pas de structure partagée. Contenus en pages libres. Chaque rédacteur invente sa propre organisation.",
                    "Typologies identifiées (actualité, fiche pratique, page de service…). Des conventions existent mais l'application est inégale.",
                    "Modèles de contenu définis dans le CMS. Taxonomies et métadonnées partagées. Les contributeurs sont guidés.",
                    "Structuration intégrée au CMS et réutilisable entre canaux. Modèles mis à jour régulièrement. Gouvernance des taxonomies.",
                ]
            },
            {
                "numero": "5.2", "nom": "Cycle de vie éditorial", "portee": "D",
                "description": "Création, publication, mise à jour, archivage — gestion des contenus dans le temps.",
                "niveaux": [
                    "Pas de cycle de vie défini. Les contenus sont publiés et rarement mis à jour. Le corpus grossit sans maîtrise.",
                    "Cycle de vie identifié pour certains types de contenus. Mais les contenus de fond ne sont pas revus.",
                    "Cycle de vie défini pour tous les types : date de revue planifiée, responsable identifié, processus d'archivage.",
                    "Cycle de vie outillé et partiellement automatisé : alertes de péremption, workflows déclenchés par les données d'usage.",
                ]
            },
            {
                "numero": "5.3", "nom": "Dette éditoriale", "portee": "D",
                "description": "Mesure et réduction des contenus obsolètes, doublons, liens cassés.",
                "niveaux": [
                    "Dette importante et non mesurée. Contenus obsolètes, doublons, liens cassés nombreux.",
                    "La dette est mesurée (audit de contenu réalisé). Plan de réduction défini. L'effort est ponctuel.",
                    "Dette faible et suivie grâce à des indicateurs réguliers. Prévention en place : règle du « un pour un ».",
                    "Dette quasi inexistante. Surveillance continue intégrée au workflow. La prévention est un réflexe.",
                ]
            },
            {
                "numero": "5.4", "nom": "Gestion des assets", "portee": "P",
                "description": "Corpus iconographique, vidéo, documents — organisation et réutilisabilité.",
                "niveaux": [
                    "Gestion individuelle et manuelle. Assets stockés localement sans organisation. Pas de traçabilité des droits.",
                    "Bibliothèque partagée mais pas intégrée aux outils de publication. Métadonnées partiellement renseignées.",
                    "DAM intégré au CMS. Métadonnées systématiques. Droits et licences suivis. Les équipes réutilisent les assets existants.",
                    "DAM centralisé, versionné, partagé. Cycle de vie des assets géré. Droits tracés de l'acquisition à l'archivage.",
                ]
            },
            {
                "numero": "5.5", "nom": "Référencement (SEO)", "portee": "P",
                "description": "Visibilité des contenus, optimisation pour les moteurs de recherche.",
                "niveaux": [
                    "Le SEO n'est pas un sujet identifié. Les contenus sont publiés sans optimisation.",
                    "Bonnes pratiques de base connues (titres, méta-descriptions). Application ponctuelle, pas de stratégie d'ensemble.",
                    "Stratégie SEO définie : mots-clés cibles, optimisation systématique, suivi de positionnement, maillage interne.",
                    "SEO intégré au processus éditorial. Analyse continue des performances. Adaptation aux évolutions des algorithmes.",
                ]
            },
            {
                "numero": "5.6", "nom": "Qualité éditoriale", "portee": "D",
                "description": "Relecture, conformité à la charte, qualité rédactionnelle.",
                "niveaux": [
                    "Pas de contrôle qualité formalisé. La qualité varie fortement d'un rédacteur à l'autre.",
                    "Relecture par un pair avant publication. Des standards de qualité existent implicitement mais pas formalisés.",
                    "Processus de relecture formalisé dans le workflow. Critères de qualité définis. Checklist avant publication.",
                    "Qualité éditoriale comme standard : checklist outillée, formation continue, amélioration des standards à partir des retours.",
                ]
            },
        ]
    },
    {
        "numero": 6,
        "nom": "Production & organisation",
        "description": "Les processus et les gens : comment on s'organise pour produire.",
        "capacites": [
            {
                "numero": "6.1", "nom": "Workflow éditorial", "portee": "D",
                "description": "Processus de validation, rôles dans le circuit de publication.",
                "niveaux": [
                    "Pas de workflow formalisé. Publication directe sans validation, ou validation informelle (accord oral).",
                    "Workflow basique : brouillon → validation → publication. Les étapes sont connues mais pas outillées.",
                    "Workflow structuré dans le CMS avec des rôles définis. Notifications automatiques. Traçabilité des validations.",
                    "Workflow intégré au cycle de vie du contenu. Tableaux de bord de production. Automatisation des étapes répétitives.",
                ]
            },
            {
                "numero": "6.2", "nom": "Gouvernance", "portee": "C",
                "description": "Pilotage de la communication numérique, instances de décision, arbitrages.",
                "niveaux": [
                    "Pilotage informel, réparti sans mandat clair. Décisions au cas par cas. Pas d'instance dédiée.",
                    "Responsabilités identifiées. Réunions de coordination régulières. Mais les décisions structurantes manquent de formalisme.",
                    "Instances de gouvernance formelles : comité éditorial, comité technique, revues de portefeuille. Décisions documentées.",
                    "Gouvernance mature : arbitrages fluides, reporting régulier, indicateurs de pilotage partagés. La gouvernance s'adapte.",
                ]
            },
            {
                "numero": "6.3", "nom": "Rôles et responsabilités", "portee": "P",
                "description": "Clarté de qui fait quoi entre SIRCOM, bureaux, prestataires, DSI.",
                "niveaux": [
                    "Les rôles ne sont pas formalisés. Qui fait quoi dépend des habitudes. Zones grises fréquentes.",
                    "Les grands rôles sont identifiés mais pas de matrice formelle. Les interfaces entre acteurs sont floues.",
                    "Matrice de responsabilités (RACI) documentée et connue de tous. Rôles clairs. Couverture des absences prévue.",
                    "Rôles révisés régulièrement. Suppléances prévues et testées. Pas de dépendance critique à une personne unique.",
                ]
            },
            {
                "numero": "6.4", "nom": "Compétences et formation", "portee": "P",
                "description": "Niveau de compétences numériques, plan de formation, montée en compétences.",
                "niveaux": [
                    "Les compétences numériques ne sont pas identifiées ni évaluées. Pas de plan de formation. Les agents se forment sur le tas.",
                    "Les besoins en compétences sont identifiés. Formations ponctuelles. Le développement des compétences est réactif.",
                    "Plan de formation structuré couvrant les compétences clés. Parcours de montée en compétences. Compétences exigées au recrutement.",
                    "Formation continue intégrée à la gestion de carrière. Communauté de pratiques active. Veille partagée. Mentorat.",
                ]
            },
            {
                "numero": "6.5", "nom": "Culture numérique", "portee": "D",
                "description": "Maturité numérique des agents, rapport aux outils et aux pratiques.",
                "niveaux": [
                    "Le numérique est perçu comme une spécialité technique. Les outils sont subis.",
                    "Le numérique est reconnu comme faisant partie du métier. Progression inégale. L'appropriation dépend des profils individuels.",
                    "La majorité des agents sont à l'aise avec les outils numériques. Le numérique fait partie du quotidien.",
                    "Le numérique fait partie de l'ADN de l'organisation. Innovation et expérimentation encouragées. Les agents sont force de proposition.",
                ]
            },
            {
                "numero": "6.6", "nom": "Gestion des prestataires", "portee": "P",
                "description": "Relation avec les prestataires (agences, ESN), maîtrise vs dépendance.",
                "niveaux": [
                    "Dépendance forte aux prestataires. Peu de compétences internalisées. Le départ du prestataire crée une crise.",
                    "Prestataires encadrés par des cahiers des charges. Transferts de compétences ponctuels. La maîtrise reste du côté prestataire.",
                    "Équilibre interne/externe maîtrisé. Suivi de qualité formalisé. Compétences clés internalisées. Changement gérable sans rupture.",
                    "Stratégie make-or-buy documentée. Compétences stratégiques internalisées. Réversibilité assurée.",
                ]
            },
        ]
    },
    {
        "numero": 7,
        "nom": "Outillage & infrastructure",
        "description": "Le SI de la communication : les outils qui soutiennent les capacités métier.",
        "capacites": [
            {
                "numero": "7.1", "nom": "CMS et publication", "portee": "P",
                "description": "Outils de gestion et publication de contenus web, niveau d'appropriation.",
                "niveaux": [
                    "CMS perçu comme un outil de mise en page. Utilisation basique. Les fonctionnalités avancées ne sont pas exploitées.",
                    "CMS utilisé pour gérer des contenus structurés. Fonctionnalités partiellement exploitées. Beaucoup d'utilisateurs basiques.",
                    "CMS pleinement exploité : workflows, taxonomies, API, modèles de contenu, droits d'accès. Contributeurs formés.",
                    "CMS au cœur du SI communication. Évolution continue. Intégrations actives (DAM, analytics, réseaux sociaux).",
                ]
            },
            {
                "numero": "7.2", "nom": "DAM (gestion d'assets)", "portee": "C",
                "description": "Outil de gestion des ressources numériques (images, vidéos, documents).",
                "niveaux": [
                    "Pas de DAM. Les assets sont gérés manuellement : dossiers partagés, envois par email. Doublons fréquents.",
                    "Outil de stockage centralisé avec arborescence partagée. Pas d'intégration avec les outils de publication.",
                    "DAM dédié intégré au CMS. Métadonnées renseignées systématiquement. Versions gérées. Recherche efficace.",
                    "DAM centralisé partagé entre entités. Flux automatisés. Cycle de vie des assets géré (péremption, archivage).",
                ]
            },
            {
                "numero": "7.3", "nom": "Outils réseaux sociaux", "portee": "P",
                "description": "Plateformes de gestion, planification, modération des réseaux sociaux.",
                "niveaux": [
                    "Publication directe sur chaque plateforme. Pas d'outil de gestion centralisé.",
                    "Outil de planification utilisé. Couverture partielle des comptes. Modération centralisée sur les principaux comptes.",
                    "Plateforme de social media management partagée. Tous les comptes gérés. Workflow de validation pour publications sensibles.",
                    "Outil intégré au SI communication (calendrier éditorial, CMS, analytics). Reporting consolidé.",
                ]
            },
            {
                "numero": "7.4", "nom": "Analytics et mesure", "portee": "P",
                "description": "Outils de mesure d'audience, tableaux de bord, exploitation des données.",
                "niveaux": [
                    "Pas de mesure d'audience, ou outil installé mais non exploité. Pas de culture de la mesure.",
                    "Outil en place (ex : Matomo). Consultation ponctuelle des métriques de base. Rapports sur demande.",
                    "Tableaux de bord structurés par canal. KPI définis et suivis. Analyse régulière partagée en comité.",
                    "Analytics cross-canal consolidés. Données exploitées pour les décisions stratégiques. Culture de la donnée installée.",
                ]
            },
            {
                "numero": "7.5", "nom": "CRM / relation citoyen", "portee": "P",
                "description": "Outils de gestion de la relation avec les publics.",
                "niveaux": [
                    "Pas d'outil de gestion de la relation. Interactions gérées par canal sans vision d'ensemble.",
                    "Outil de newsletter et formulaires de contact. Bases de contacts par canal, sans croisement.",
                    "CRM unifié multicanal. Vision consolidée des interactions. Segmentation exploitable. Historique tracé.",
                    "CRM intégré au SI ministériel. Personnalisation des communications. Suivi des parcours citoyen. RGPD native.",
                ]
            },
            {
                "numero": "7.6", "nom": "Intégration SI", "portee": "C",
                "description": "Connexion entre le SI communication et le SI global du ministère.",
                "niveaux": [
                    "Le SI communication est isolé. Pas de connexion au SI ministériel. Saisies redondantes et données non synchronisées.",
                    "Quelques intégrations ponctuelles (SSO, annuaire). Pas de vision d'architecture. Connexions fragiles.",
                    "Intégration structurée : référentiels partagés, SSO, API documentées. Les données circulent de manière maîtrisée.",
                    "SI communication pleinement intégré. Interopérabilité native. Architecture documentée et gouvernée.",
                ]
            },
            {
                "numero": "7.7", "nom": "Hébergement et exploitation", "portee": "C",
                "description": "Infrastructure, hébergement, supervision, performance.",
                "niveaux": [
                    "Hébergement subi. Pas de supervision. Les problèmes sont découverts par les usagers.",
                    "Hébergement adapté. Supervision basique (disponibilité). Interventions réactives.",
                    "Infrastructure moderne (containers, cloud). Supervision proactive. Alertes automatisées. Déploiements maîtrisés.",
                    "Infrastructure évolutive et résiliente. CI/CD. Plan de reprise testé. Capacité d'absorber les pics.",
                ]
            },
            {
                "numero": "7.8", "nom": "Sécurité et conformité", "portee": "C",
                "description": "Sécurité des outils, conformité RGPD, homologation.",
                "niveaux": [
                    "Sécurité et RGPD traités de manière réactive. Pas d'homologation. Traitements de données personnelles pas tous identifiés.",
                    "Processus de conformité identifiés. Registre des traitements en cours. Audits ponctuels.",
                    "Sécurité et RGPD intégrés dès la conception. Homologation des outils. Audits réguliers. Conformité > 90 %.",
                    "Amélioration continue. Veille réglementaire active. Conformité proche de 100 %. Les évolutions réglementaires sont anticipées.",
                ]
            },
            {
                "numero": "7.9", "nom": "IA et automatisation", "portee": "P",
                "description": "Usage de l'IA dans la communication : chatbots, aide à la rédaction, personnalisation.",
                "niveaux": [
                    "Pas d'usage de l'IA dans la communication. Le sujet est observé de loin ou pas du tout.",
                    "Expérimentations ponctuelles : aide à la rédaction (LLM), chatbot simple, traduction automatique. Usages non encadrés.",
                    "Usages identifiés et encadrés par une charte d'usage et un cadre éthique. Outils déployés sur des cas précis. Formation.",
                    "IA intégrée aux processus de communication. Cadre éthique formalisé et appliqué. Veille active. Évaluation régulière.",
                ]
            },
        ]
    },
]


def seed_referentiel():
    """Insère le référentiel v2 dans la base de données si absent."""
    if ReferentielVersion.query.filter_by(label="v2.0").first():
        return False  # Déjà présent

    ref = ReferentielVersion(
        label="v2.0",
        description="Référentiel de maturité de la communication numérique ministérielle — version 2.0",
        cible="organisation",
        is_active=True,
    )
    db.session.add(ref)
    db.session.flush()  # pour obtenir ref.id

    for dim_data in DIMENSIONS:
        dim = Dimension(
            referentiel_id=ref.id,
            numero=dim_data["numero"],
            nom=dim_data["nom"],
            description=dim_data["description"],
        )
        db.session.add(dim)
        db.session.flush()

        for cap_data in dim_data["capacites"]:
            cap = Capacite(
                dimension_id=dim.id,
                numero=cap_data["numero"],
                nom=cap_data["nom"],
                description=cap_data["description"],
                portee=cap_data["portee"],
            )
            db.session.add(cap)
            db.session.flush()

            for i, desc in enumerate(cap_data["niveaux"], start=1):
                niv = NiveauCritere(
                    capacite_id=cap.id,
                    niveau=i,
                    nom=NOMS_NIVEAUX[i],
                    description=desc,
                )
                db.session.add(niv)

    db.session.commit()
    return True


# ──────────────────────────────────────────────
# Mini-référentiels thématiques
# ──────────────────────────────────────────────

MINI_REFERENTIELS = [
    # ── 1. Accessibilité Organisation ──
    {
        "label": "Accessibilité-org-v1",
        "description": "Maturité accessibilité numérique — volet organisation",
        "cible": "organisation",
        "is_active": False,
        "noms_niveaux": {1: "Émergent", 2: "Structuré", 3: "Intégré", 4: "Pérenne"},
        "dimensions": [
            {
                "numero": 1, "nom": "Pilotage & engagement",
                "description": "Portage stratégique et moyens dédiés à l'accessibilité numérique.",
                "capacites": [
                    {"numero": "1.1", "nom": "Engagement de la direction", "portee": "C",
                     "description": "La direction porte-t-elle l'accessibilité comme un objectif stratégique ?",
                     "niveaux": [
                         "L'accessibilité n'est pas un sujet identifié par la direction. Aucune mention dans les documents stratégiques.",
                         "La direction reconnaît l'obligation légale mais ne porte pas le sujet activement. Quelques initiatives isolées.",
                         "L'accessibilité est inscrite dans la feuille de route. Un·e référent·e est identifié·e. La direction arbitre en faveur de l'accessibilité.",
                         "L'accessibilité est un critère de décision systématique. La direction communique sur les résultats. Le sujet est porté au plus haut niveau.",
                     ]},
                    {"numero": "1.2", "nom": "Schéma pluriannuel", "portee": "D",
                     "description": "Existence et mise en œuvre d'un schéma pluriannuel de mise en accessibilité.",
                     "niveaux": [
                         "Pas de schéma pluriannuel publié, ou schéma obsolète non mis à jour.",
                         "Schéma publié mais générique, sans actions concrètes ni calendrier précis.",
                         "Schéma détaillé avec actions, calendrier, responsables identifiés. Suivi annuel effectif.",
                         "Schéma intégré au pilotage global, mis à jour régulièrement, bilan publié. Aligné avec la stratégie numérique.",
                     ]},
                    {"numero": "1.3", "nom": "Budget dédié", "portee": "D",
                     "description": "Allocation de ressources financières spécifiques à l'accessibilité.",
                     "niveaux": [
                         "Pas de budget identifié pour l'accessibilité. Les audits et corrections sont financés au cas par cas.",
                         "Budget ponctuel (un audit, une formation) mais pas de ligne récurrente.",
                         "Ligne budgétaire annuelle dédiée : audits, outils, formation, correction. Suffisante pour les besoins identifiés.",
                         "Budget pluriannuel sanctuarisé, révisé chaque année. Intègre la maintenance et l'amélioration continue.",
                     ]},
                    {"numero": "1.4", "nom": "Suivi & indicateurs", "portee": "D",
                     "description": "Pilotage par indicateurs : taux de conformité, avancement du schéma, nombre de sites audités.",
                     "niveaux": [
                         "Pas d'indicateurs de suivi. L'état de conformité des sites n'est pas connu.",
                         "Suivi ponctuel : quelques taux de conformité connus mais pas consolidés. Pas de tableau de bord.",
                         "Tableau de bord avec indicateurs clés (% conformité par site, avancement schéma). Suivi trimestriel.",
                         "Indicateurs intégrés au reporting de la DSI/DNUM. Benchmark entre sites. Trajectoire de progression suivie.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Compétences & culture",
                "description": "Montée en compétences et diffusion de la culture accessibilité dans l'organisation.",
                "capacites": [
                    {"numero": "2.1", "nom": "Référent accessibilité", "portee": "D",
                     "description": "Existence d'un·e référent·e identifié·e avec un mandat clair.",
                     "niveaux": [
                         "Pas de référent. Le sujet est porté par bonne volonté individuelle.",
                         "Un·e référent·e désigné·e mais sans mandat formel ni temps dédié. Rôle consultatif.",
                         "Référent·e avec mandat, temps dédié, rattachement hiérarchique clair. Reconnu·e comme point de contact.",
                         "Équipe accessibilité structurée (ou réseau de référents). Expertise interne reconnue. Capacité d'accompagnement des projets.",
                     ]},
                    {"numero": "2.2", "nom": "Formation des équipes", "portee": "P",
                     "description": "Les équipes (dev, design, contenu, chef de projet) sont-elles formées ?",
                     "niveaux": [
                         "Pas de formation. Les équipes découvrent le RGAA au moment de l'audit.",
                         "Quelques formations ponctuelles (sensibilisation). Pas de plan structuré.",
                         "Plan de formation par profil (dev, design, rédacteurs, CP). Formations régulières. Parcours d'intégration.",
                         "Culture d'apprentissage continu. Veille partagée, communauté de pratique, certifications encouragées.",
                     ]},
                    {"numero": "2.3", "nom": "Intégration dans les processus", "portee": "P",
                     "description": "L'accessibilité est-elle intégrée dans le cycle de vie des projets ?",
                     "niveaux": [
                         "L'accessibilité est traitée en fin de projet (audit avant MEP, corrections a posteriori).",
                         "L'accessibilité est mentionnée dans les cahiers des charges mais pas systématiquement vérifiée.",
                         "Intégrée aux revues de conception, aux tests, à la recette. Critères d'accessibilité dans la Definition of Done.",
                         "L'accessibilité est native dans tous les processus. Tests automatisés en CI. Revues de code incluent l'accessibilité.",
                     ]},
                    {"numero": "2.4", "nom": "Culture & sensibilisation", "portee": "P",
                     "description": "Le sujet dépasse-t-il le cercle des experts ?",
                     "niveaux": [
                         "Sujet perçu comme technique et contraignant. Peu de personnes concernées.",
                         "Sensibilisation ponctuelle (journée mondiale, présentation interne). Intérêt croissant mais limité.",
                         "Sensibilisation régulière, témoignages d'usagers, ateliers de mise en situation. Le sujet est compris au-delà des équipes techniques.",
                         "L'accessibilité fait partie de la culture de l'organisation. Réflexe naturel. Portée par tous les métiers.",
                     ]},
                ]
            },
        ]
    },
    # ── 2. Accessibilité Site ──
    {
        "label": "Accessibilité-site-v1",
        "description": "Conformité et qualité accessibilité — volet site web",
        "cible": "site",
        "is_active": False,
        "noms_niveaux": {1: "Insuffisant", 2: "Partiel", 3: "Conforme"},
        "dimensions": [
            {
                "numero": 1, "nom": "Conformité technique",
                "description": "Respect du RGAA et des obligations légales d'accessibilité.",
                "capacites": [
                    {"numero": "1.1", "nom": "Taux de conformité RGAA", "portee": "D",
                     "description": "Résultat du dernier audit de conformité au RGAA.",
                     "niveaux": [
                         "Taux inconnu ou < 50%. Nombreuses non-conformités bloquantes.",
                         "Taux entre 50% et 75%. Non-conformités identifiées, plan de correction en cours.",
                         "Taux > 75%. Non-conformités résiduelles mineures. Dérogations documentées et justifiées.",
                     ]},
                    {"numero": "1.2", "nom": "Déclaration d'accessibilité", "portee": "D",
                     "description": "Présence, complétude et mise à jour de la déclaration obligatoire.",
                     "niveaux": [
                         "Absente ou non conforme (pas de mention, ou simple mention « en cours »).",
                         "Déclaration publiée mais incomplète (manque le plan d'action, les dérogations, ou la date d'audit).",
                         "Déclaration complète, à jour, conforme au modèle légal. Lien visible depuis toutes les pages.",
                     ]},
                    {"numero": "1.3", "nom": "Audit et fréquence", "portee": "D",
                     "description": "Le site fait-il l'objet d'audits réguliers et fiables ?",
                     "niveaux": [
                         "Pas d'audit réalisé, ou audit de plus de 3 ans.",
                         "Audit réalisé (externe ou auto-évaluation) mais ponctuel. Pas de suivi post-audit structuré.",
                         "Audits réguliers (a minima à chaque refonte majeure). Suivi des corrections. Re-test après correction.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Qualité de l'expérience",
                "description": "Qualité réelle de l'expérience pour les utilisateurs en situation de handicap.",
                "capacites": [
                    {"numero": "2.1", "nom": "Navigation & structure", "portee": "D",
                     "description": "Le site est-il navigable au clavier et avec un lecteur d'écran ?",
                     "niveaux": [
                         "Navigation au clavier impossible ou très dégradée. Pas de landmarks, titres de pages génériques.",
                         "Navigation au clavier fonctionnelle sur les parcours principaux. Structure de titres cohérente.",
                         "Navigation fluide au clavier et lecteur d'écran. Landmarks, skip links, titres hiérarchisés.",
                     ]},
                    {"numero": "2.2", "nom": "Contenus accessibles", "portee": "P",
                     "description": "Les contenus (textes, images, documents, vidéos) sont-ils accessibles ?",
                     "niveaux": [
                         "Images sans alternatives, documents PDF non balisés, vidéos sans sous-titres.",
                         "Alternatives textuelles sur les images principales. Certains documents accessibles. Sous-titres sur les vidéos récentes.",
                         "Politique systématique : toute image a une alternative, documents PDF balisés, vidéos sous-titrées.",
                     ]},
                    {"numero": "2.3", "nom": "Formulaires & interactions", "portee": "D",
                     "description": "Les formulaires et composants interactifs sont-ils accessibles ?",
                     "niveaux": [
                         "Formulaires sans labels associés, messages d'erreur non explicites, composants custom non accessibles.",
                         "Labels présents sur la plupart des champs. Messages d'erreur identifiés. Quelques composants custom à améliorer.",
                         "Tous les formulaires sont accessibles : labels, erreurs en temps réel, focus géré, composants ARIA conformes.",
                     ]},
                    {"numero": "2.4", "nom": "Retour utilisateur", "portee": "P",
                     "description": "Existe-t-il un canal de signalement des problèmes d'accessibilité ?",
                     "niveaux": [
                         "Pas de moyen de signaler un problème d'accessibilité (obligation légale non respectée).",
                         "Adresse email de contact mentionnée dans la déclaration, mais pas de processus de traitement structuré.",
                         "Canal de signalement visible, processus de traitement défini avec délais, retour systématique à l'usager.",
                     ]},
                ]
            },
        ]
    },
    # ── 3. Design Organisation (référentiel complet MEF/MIWEB) ──
    {
        "label": "Design-org-v1",
        "description": "Maturité des pratiques design — volet organisation (adapté du référentiel MEF/MIWEB)",
        "cible": "organisation",
        "is_active": False,
        "noms_niveaux": {1: "Absent", 2: "Engagé", 3: "Systématisé"},
        "dimensions": [
            {
                "numero": 1, "nom": "Recherche utilisateur",
                "description": "Exploration amont : capacité à comprendre le contexte et les usagers avant de concevoir.",
                "capacites": [
                    {"numero": "1.1", "nom": "Benchmark / analyse concurrentielle", "portee": "D",
                     "description": "Connaissance de l'existant et de l'environnement.",
                     "niveaux": [
                         "Pas de benchmark réalisé, ou veille non documentée.",
                         "Benchmark réalisé de manière ponctuelle, grille non formalisée, résultats partagés de manière informelle.",
                         "Benchmark structuré avec grille d'analyse, documenté, partagé avec les parties prenantes, mis à jour si le contexte évolue.",
                     ]},
                    {"numero": "1.2", "nom": "Entretiens métiers / parties prenantes", "portee": "D",
                     "description": "Recueil des besoins et contraintes auprès des acteurs internes.",
                     "niveaux": [
                         "Aucun entretien, ou échanges informels non documentés.",
                         "Quelques entretiens réalisés, guide d'entretien existant mais pas systématique, synthèse partielle.",
                         "Entretiens systématiques avec grille structurée, synthèse formalisée et partagée, verbatims exploitables.",
                     ]},
                    {"numero": "1.3", "nom": "Recherche terrain / observation", "portee": "D",
                     "description": "Observation du contexte réel d'utilisation.",
                     "niveaux": [
                         "Pas d'observation du contexte réel d'utilisation.",
                         "Observation ponctuelle (1-2 sessions), sans protocole formalisé.",
                         "Recherche contextuelle ou ethnographique structurée, protocole documenté, insights actionnables produits.",
                     ]},
                    {"numero": "1.4", "nom": "Enquêtes quantitatives", "portee": "P",
                     "description": "Recueil de données quantitatives sur les usages et la satisfaction.",
                     "niveaux": [
                         "Pas d'enquête quantitative menée.",
                         "Enquête ponctuelle (satisfaction post-lancement, sondage unique), pas de suivi longitudinal.",
                         "Enquêtes récurrentes avec suivi dans le temps, croisement avec analytics, données comparables entre évaluations.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Conception & prototypage",
                "description": "Formalisation des solutions et validation avant développement.",
                "capacites": [
                    {"numero": "2.1", "nom": "Personas / profils utilisateurs", "portee": "P",
                     "description": "Formalisation de la connaissance des publics cibles.",
                     "niveaux": [
                         "Pas de personas ou profils utilisateurs formalisés.",
                         "Personas créés mais non maintenus, utilisés de manière ponctuelle.",
                         "Personas documentés, mis à jour régulièrement, utilisés dans les arbitrages de conception et priorisation.",
                     ]},
                    {"numero": "2.2", "nom": "Prototypage / maquettage", "portee": "D",
                     "description": "Matérialisation des solutions avant développement.",
                     "niveaux": [
                         "Pas de maquettes : le développement se fait directement à partir de spécifications fonctionnelles.",
                         "Maquettes ou wireframes produits, mais pas testés avec des usagers avant le développement.",
                         "Prototypes itératifs (basse puis haute fidélité), testés avec des usagers, itérés avant passage en développement.",
                     ]},
                    {"numero": "2.3", "nom": "Tests utilisateurs", "portee": "D",
                     "description": "Validation des solutions avec de vrais usagers.",
                     "niveaux": [
                         "Aucun test avec des usagers réels.",
                         "Tests ponctuels (1 cycle, souvent en fin de projet), recommandations partiellement intégrées.",
                         "Tests récurrents à chaque itération majeure, panel diversifié, recommandations systématiquement traitées.",
                     ]},
                    {"numero": "2.4", "nom": "Focus groupes / co-conception", "portee": "P",
                     "description": "Implication des usagers et agents dans la conception.",
                     "niveaux": [
                         "Aucun atelier impliquant des usagers ou des agents.",
                         "Atelier(s) ponctuel(s), format pas toujours structuré, résultats peu exploités.",
                         "Co-conception structurée avec usagers et/ou agents, ateliers récurrents, résultats intégrés aux décisions.",
                     ]},
                ]
            },
            {
                "numero": 3, "nom": "Évaluation & amélioration continue",
                "description": "Capacité à évaluer la qualité UX et à itérer après la mise en ligne.",
                "capacites": [
                    {"numero": "3.1", "nom": "Audit UX avant mise en ligne", "portee": "D",
                     "description": "Revue de la qualité UX avant publication.",
                     "niveaux": [
                         "Pas de revue UX avant la mise en ligne.",
                         "Revue informelle par l'équipe projet, sans grille ni rapport formalisé.",
                         "Audit UX formalisé avec grille d'évaluation, rapport de recommandations, suivi de la prise en compte.",
                     ]},
                    {"numero": "3.2", "nom": "Itération post-lancement", "portee": "D",
                     "description": "Capacité à améliorer le produit après sa sortie.",
                     "niveaux": [
                         "Pas d'itération UX après la mise en ligne, le produit est « figé ».",
                         "Corrections ponctuelles sur la base de retours (support, analytics), mais pas de cycle structuré.",
                         "Cycle d'amélioration continue piloté par la donnée UX : analytics + retours usagers → priorisation → itération.",
                     ]},
                    {"numero": "3.3", "nom": "Satisfaction usagers", "portee": "P",
                     "description": "Mesure de la satisfaction des usagers du produit.",
                     "niveaux": [
                         "Score < 5/10 ou retours majoritairement négatifs, irritants majeurs identifiés.",
                         "Score entre 5 et 7/10, retours mitigés, des points positifs mais des irritants persistants.",
                         "Score > 7/10, retours globalement positifs, usagers satisfaits de l'expérience.",
                     ]},
                ]
            },
            {
                "numero": 4, "nom": "Gouvernance design",
                "description": "Organisation de la fonction design et intégration dans les processus projet.",
                "capacites": [
                    {"numero": "4.1", "nom": "Compétences design dans l'équipe", "portee": "D",
                     "description": "Présence et niveau de compétences design.",
                     "niveaux": [
                         "Aucune compétence design dans l'équipe, pas de recours possible identifié.",
                         "Compétence partielle (CdP avec sensibilité UX, ou design mobilisable ponctuellement).",
                         "Profil design dédié dans l'équipe (interne ou prestataire identifié), expertise reconnue.",
                     ]},
                    {"numero": "4.2", "nom": "Phase d'intervention du design", "portee": "D",
                     "description": "À quel moment le design intervient-il dans le cycle projet ?",
                     "niveaux": [
                         "Le design intervient en fin de chaîne (habillage, recette) ou jamais.",
                         "Le design intervient en phase de conception, après le cadrage fonctionnel.",
                         "Le design est associé dès le cadrage. Il contribue à la définition du problème, pas seulement de la solution.",
                     ]},
                    {"numero": "4.3", "nom": "Processus de validation UX", "portee": "P",
                     "description": "Circuit formel de validation des livrables design.",
                     "niveaux": [
                         "Pas de validation UX formelle. Les arbitrages visuels sont faits par la hiérarchie.",
                         "Revue informelle par l'équipe projet, sans grille ni rapport.",
                         "Processus de validation formalisé : revue UX avec grille, rapport, suivi de la prise en compte.",
                     ]},
                    {"numero": "4.4", "nom": "Design system", "portee": "P",
                     "description": "Utilisation d'un design system partagé (DSFR ou interne).",
                     "niveaux": [
                         "Pas de design system. Chaque projet invente ses propres composants.",
                         "Le DSFR est connu mais appliqué de manière partielle ou incohérente.",
                         "Le DSFR est systématiquement utilisé. Composants custom documentés et partagés.",
                     ]},
                ]
            },
        ]
    },
    # ── 4. Design Site (référentiel complet MEF/MIWEB) ──
    {
        "label": "Design-site-v1",
        "description": "Qualité design et expérience utilisateur — volet site web (adapté du référentiel MEF/MIWEB)",
        "cible": "site",
        "is_active": False,
        "noms_niveaux": {1: "Insuffisant", 2: "Partiel", 3: "Conforme"},
        "dimensions": [
            {
                "numero": 1, "nom": "Conformité & standards",
                "description": "Respect des standards visuels et réglementaires de l'État.",
                "capacites": [
                    {"numero": "1.1", "nom": "Conformité DSFR", "portee": "D",
                     "description": "Le site applique-t-il le Design Système de l'État ?",
                     "niveaux": [
                         "DSFR non implémenté ou version obsolète. Agrément SIG non demandé.",
                         "DSFR partiellement implémenté. Agrément en cours. Certaines pages ou composants non conformes.",
                         "DSFR correctement implémenté, version à jour, agrément obtenu. Composants custom conformes à l'esprit DSFR.",
                     ]},
                    {"numero": "1.2", "nom": "Agrément SIG", "portee": "D",
                     "description": "Statut de l'agrément auprès du Service d'information du Gouvernement.",
                     "niveaux": [
                         "Agrément non demandé ou refusé avec non-conformités non traitées.",
                         "Demande d'agrément en cours, corrections en progression.",
                         "Agrément obtenu et maintenu à jour.",
                     ]},
                    {"numero": "1.3", "nom": "Cohérence visuelle", "portee": "P",
                     "description": "L'interface est-elle visuellement cohérente sur l'ensemble du site ?",
                     "niveaux": [
                         "Incohérences visibles : mélange de styles, composants disparates, pas de grille claire.",
                         "Cohérence globale respectée mais quelques écarts (pages legacy, modules tiers non stylés).",
                         "Interface homogène sur l'ensemble du site. Composants réutilisés. Identité visuelle constante.",
                     ]},
                    {"numero": "1.4", "nom": "Responsive & mobile", "portee": "D",
                     "description": "Le site est-il utilisable sur tous les écrans ?",
                     "niveaux": [
                         "Site non responsive ou très dégradé sur mobile. Navigation difficile.",
                         "Responsive sur les pages principales. Quelques problèmes sur les formulaires complexes ou les tableaux.",
                         "Expérience mobile soignée. Tous les parcours testés sur mobile. Performance optimisée pour les connexions lentes.",
                     ]},
                    {"numero": "1.5", "nom": "Mentions légales & conformité", "portee": "D",
                     "description": "Conformité aux obligations légales (CGU, RGPD, cookies).",
                     "niveaux": [
                         "Mentions légales absentes ou non conformes.",
                         "Mentions légales présentes mais incomplètes (manque politique cookies, RGPD partiel).",
                         "Mentions légales conformes et à jour. Politique de cookies claire. RGPD respecté.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Qualité de l'expérience utilisateur",
                "description": "Qualité réelle de l'expérience pour les usagers du site.",
                "capacites": [
                    {"numero": "2.1", "nom": "Positionnement & différenciation", "portee": "C",
                     "description": "Le message du site est-il clair et différencié dans l'écosystème ?",
                     "niveaux": [
                         "Message flou ou redondant avec un autre produit. L'usager ne comprend pas pourquoi ce site existe.",
                         "Message identifié mais chevauchements avec d'autres sites sur certaines thématiques.",
                         "Message clair, unique, bien différencié. L'usager comprend immédiatement la valeur propre du site.",
                     ]},
                    {"numero": "2.2", "nom": "Clarté des parcours", "portee": "P",
                     "description": "Les parcours principaux sont-ils clairs, courts et compréhensibles ?",
                     "niveaux": [
                         "Parcours confus, trop d'étapes, architecture de l'information non lisible. L'usager se perd.",
                         "Parcours principaux identifiés et fonctionnels. Quelques points de friction connus mais non traités.",
                         "Parcours optimisés, testés avec des usagers. Arborescence claire. Aide contextuelle quand nécessaire.",
                     ]},
                    {"numero": "2.3", "nom": "Qualité rédactionnelle", "portee": "P",
                     "description": "Les contenus sont-ils rédigés en langage clair et structuré ?",
                     "niveaux": [
                         "Jargon administratif, phrases longues, pas de structuration. Contenu écrit pour l'administration, pas pour l'usager.",
                         "Effort de simplification sur les contenus principaux. Titres explicites. Certaines pages encore techniques.",
                         "Langage clair appliqué systématiquement. Contenus structurés, testés, maintenus. Charte rédactionnelle respectée.",
                     ]},
                    {"numero": "2.4", "nom": "Performance perçue", "portee": "D",
                     "description": "Le site est-il rapide et fluide du point de vue de l'usager ?",
                     "niveaux": [
                         "Temps de chargement > 5s, interactions lentes, impression de lourdeur.",
                         "Performance correcte (< 3s) sur les pages principales. Quelques pages lentes (recherche, tableaux).",
                         "Performance optimisée : Core Web Vitals au vert, chargement progressif, transitions fluides.",
                     ]},
                    {"numero": "2.5", "nom": "Satisfaction usagers", "portee": "P",
                     "description": "La satisfaction des usagers est-elle mesurée et prise en compte ?",
                     "niveaux": [
                         "Aucune mesure de satisfaction. Pas de retour usager exploité.",
                         "Enquête ponctuelle ou bouton de feedback. Résultats analysés mais pas systématiquement exploités.",
                         "Mesure récurrente (enquête, UX score, analytics comportemental). Résultats intégrés dans la priorisation produit.",
                     ]},
                    {"numero": "2.6", "nom": "Éco-conception", "portee": "P",
                     "description": "L'impact environnemental du site est-il pris en compte ?",
                     "niveaux": [
                         "Éco-conception non prise en compte. Poids des pages et sobriété non mesurés.",
                         "Quelques bonnes pratiques appliquées (optimisation images, limitation vidéos). Pas de démarche structurée.",
                         "Démarche éco-conception structurée (RGESN ou équivalent). Mesure régulière de l'impact. Arbitrages documentés.",
                     ]},
                ]
            },
        ]
    },
    # ── 5. Data Organisation ──
    {
        "label": "Data-org-v1",
        "description": "Maturité data et gouvernance des données — volet organisation",
        "cible": "organisation",
        "is_active": False,
        "noms_niveaux": {1: "Émergent", 2: "Structuré", 3: "Intégré", 4: "Pérenne"},
        "dimensions": [
            {
                "numero": 1, "nom": "Gouvernance data",
                "description": "Stratégie, rôles et cadre réglementaire autour des données.",
                "capacites": [
                    {"numero": "1.1", "nom": "Stratégie data", "portee": "C",
                     "description": "L'organisation a-t-elle une stratégie data formalisée ?",
                     "niveaux": [
                         "Pas de stratégie data. Les données sont gérées au fil de l'eau par chaque projet.",
                         "Une vision existe mais elle est informelle. Quelques initiatives data portées par des individus motivés.",
                         "Stratégie data formalisée, feuille de route avec jalons, alignée sur la stratégie numérique globale.",
                         "Stratégie data vivante, revue annuellement. Budget dédié. La donnée est un actif stratégique reconnu.",
                     ]},
                    {"numero": "1.2", "nom": "Rôles & responsabilités", "portee": "D",
                     "description": "Les rôles data sont-ils identifiés (CDO, DPO, référents, data engineers) ?",
                     "niveaux": [
                         "Pas de rôle data identifié. La gestion des données incombe aux développeurs projet par projet.",
                         "Un DPO existe (obligation légale). Quelques profils data mais sans coordination.",
                         "Organisation data structurée : CDO ou équivalent, référents métier, data engineers. Responsabilités claires.",
                         "Communauté data active. Réseau de référents dans les directions. Filière data reconnue.",
                     ]},
                    {"numero": "1.3", "nom": "Cadre éthique & RGPD", "portee": "D",
                     "description": "L'utilisation des données respecte-t-elle un cadre éthique et réglementaire ?",
                     "niveaux": [
                         "Conformité RGPD minimale (registre de traitement). Pas de réflexion éthique sur l'usage des données.",
                         "RGPD respecté formellement. Sensibilisation des équipes. Pas de cadre éthique au-delà du réglementaire.",
                         "Cadre éthique formalisé pour l'usage des données (IA, profilage, open data). PIA systématiques.",
                         "Éthique data intégrée dans la culture. Comité éthique ou processus de revue. Transparence sur les algorithmes.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Compétences & culture data",
                "description": "Montée en compétences et diffusion de la culture data.",
                "capacites": [
                    {"numero": "2.1", "nom": "Littératie data", "portee": "P",
                     "description": "Les agents comprennent-ils les données qu'ils manipulent ?",
                     "niveaux": [
                         "Les données sont manipulées sans compréhension (copier-coller, pas d'esprit critique sur les chiffres).",
                         "Quelques agents formés (Excel avancé, notions de dataviz). La majorité consomme sans questionner.",
                         "Formation data intégrée aux parcours métier. Les agents savent lire un dashboard, poser des questions aux données.",
                         "Culture data-driven. Les décisions s'appuient sur les données. Les agents sont autonomes dans l'exploration.",
                     ]},
                    {"numero": "2.2", "nom": "Outillage & accès", "portee": "D",
                     "description": "Les équipes disposent-elles d'outils adaptés pour exploiter les données ?",
                     "niveaux": [
                         "Pas d'outil de datavisualisation ou de requêtage accessible aux métiers. Tout passe par la DSI.",
                         "Quelques outils disponibles (Excel, BI ponctuel) mais pas d'accès self-service aux données.",
                         "Plateforme data accessible aux métiers. Dashboards partagés. Catalogue de données consultable.",
                         "Data platform mature : accès self-service, API internes, documentation automatisée, monitoring qualité.",
                     ]},
                    {"numero": "2.3", "nom": "Partage & documentation", "portee": "P",
                     "description": "Les jeux de données internes sont-ils documentés et partagés ?",
                     "niveaux": [
                         "Données en silos. Chaque direction a ses propres fichiers, pas de vision transverse.",
                         "Quelques jeux de données partagés de manière informelle. Pas de catalogue.",
                         "Catalogue de données interne. Métadonnées documentées. Responsables identifiés par jeu de données.",
                         "Données internes accessibles et documentées par défaut. Politique d'open data interne.",
                     ]},
                ]
            },
        ]
    },
    # ── 6. Data Site ──
    {
        "label": "Data-site-v1",
        "description": "Mesure, transparence et ouverture des données — volet site web",
        "cible": "site",
        "is_active": False,
        "noms_niveaux": {1: "Insuffisant", 2: "Partiel", 3: "Conforme"},
        "dimensions": [
            {
                "numero": 1, "nom": "Mesure & analytics",
                "description": "Capacité du site à mesurer et exploiter les données d'usage.",
                "capacites": [
                    {"numero": "1.1", "nom": "Outil de mesure", "portee": "D",
                     "description": "Le site dispose-t-il d'un outil de mesure d'audience respectueux du RGPD ?",
                     "niveaux": [
                         "Pas d'outil de mesure, ou outil non conforme RGPD (Google Analytics sans consentement).",
                         "Outil en place (Matomo, AT Internet…) mais configuration partielle.",
                         "Outil conforme RGPD correctement configuré. Suivi des pages, événements, conversions.",
                     ]},
                    {"numero": "1.2", "nom": "Qualité du suivi", "portee": "D",
                     "description": "Les indicateurs clés sont-ils définis et suivis ?",
                     "niveaux": [
                         "Pas d'indicateurs définis. Les données brutes existent mais personne ne les regarde.",
                         "Quelques KPIs suivis (pages vues, visiteurs) mais pas de tableau de bord.",
                         "KPIs définis par objectif du site. Tableau de bord partagé. Revue mensuelle.",
                     ]},
                    {"numero": "1.3", "nom": "Exploitation des données", "portee": "P",
                     "description": "Les données analytics sont-elles exploitées pour améliorer le site ?",
                     "niveaux": [
                         "Les données ne sont pas exploitées. Pas de lien entre analytics et décisions produit.",
                         "Analyse ponctuelle pour justifier des évolutions. Pas de démarche proactive.",
                         "Démarche data-driven : les analytics alimentent le backlog, valident les hypothèses.",
                     ]},
                ]
            },
            {
                "numero": 2, "nom": "Transparence & ouverture",
                "description": "Conformité réglementaire et contribution à l'ouverture des données.",
                "capacites": [
                    {"numero": "2.1", "nom": "Conformité cookies & traceurs", "portee": "D",
                     "description": "La gestion des cookies est-elle conforme au RGPD ?",
                     "niveaux": [
                         "Pas de bandeau cookies, ou consentement non recueilli correctement.",
                         "Bandeau cookies présent mais configuration imparfaite.",
                         "Gestion des cookies conforme : consentement libre, refus aussi simple qu'acceptation.",
                     ]},
                    {"numero": "2.2", "nom": "Open data", "portee": "P",
                     "description": "Le site contribue-t-il à l'ouverture des données publiques ?",
                     "niveaux": [
                         "Pas de données ouvertes. Le site ne publie ni ne référence de jeux de données.",
                         "Quelques jeux de données publiés sur data.gouv.fr mais pas maintenus.",
                         "Politique d'ouverture : jeux de données identifiés, publiés, documentés, mis à jour.",
                     ]},
                    {"numero": "2.3", "nom": "API & interopérabilité", "portee": "D",
                     "description": "Le site expose-t-il des données via des API documentées ?",
                     "niveaux": [
                         "Pas d'API. Les données du site ne sont accessibles qu'en naviguant sur les pages.",
                         "API existante mais non documentée ou non maintenue. Usage interne uniquement.",
                         "API documentée (OpenAPI/Swagger), versionnée, monitorée. Référencée sur api.gouv.fr.",
                     ]},
                ]
            },
        ]
    },
]


def seed_mini_referentiels():
    """Insère les mini-référentiels de test si absents."""
    for ref_data in MINI_REFERENTIELS:
        if ReferentielVersion.query.filter_by(label=ref_data["label"]).first():
            continue

        ref = ReferentielVersion(
            label=ref_data["label"],
            description=ref_data["description"],
            cible=ref_data["cible"],
            is_active=ref_data.get("is_active", False),
        )
        db.session.add(ref)
        db.session.flush()

        noms_niveaux = ref_data["noms_niveaux"]

        for dim_data in ref_data["dimensions"]:
            dim = Dimension(
                referentiel_id=ref.id,
                numero=dim_data["numero"],
                nom=dim_data["nom"],
                description=dim_data.get("description", ""),
            )
            db.session.add(dim)
            db.session.flush()

            for cap_data in dim_data["capacites"]:
                cap = Capacite(
                    dimension_id=dim.id,
                    numero=cap_data["numero"],
                    nom=cap_data["nom"],
                    description=cap_data.get("description", ""),
                    portee=cap_data["portee"],
                )
                db.session.add(cap)
                db.session.flush()

                for i, desc in enumerate(cap_data["niveaux"], start=1):
                    niv = NiveauCritere(
                        capacite_id=cap.id,
                        niveau=i,
                        nom=noms_niveaux[i],
                        description=desc,
                    )
                    db.session.add(niv)

    db.session.commit()


def seed_demo_entites():
    """Insère quelques entités de démo si aucune n'existe."""
    if Entite.query.first():
        return False

    entites = [
        Entite(nom="SIRCOM", type="SIRCOM", direction="SG", description="Service d'information et de communication"),
        Entite(nom="Bureau com — Affaires sociales", type="Bureau", direction="DGCS"),
        Entite(nom="Bureau com — Travail", type="Bureau", direction="DGT"),
        Entite(nom="Bureau com — Santé", type="Bureau", direction="DGS"),
        Entite(nom="Bureau com — Jeunesse", type="Bureau", direction="DJEPVA"),
    ]
    db.session.add_all(entites)
    db.session.commit()
    return True


def seed_demo_sites():
    """Insère quelques sites de démo si aucun n'existe."""
    if Site.query.first():
        return False

    sircom = Entite.query.filter_by(nom="SIRCOM").first()
    bcom_sante = Entite.query.filter_by(nom="Bureau com — Santé").first()
    bcom_travail = Entite.query.filter_by(nom="Bureau com — Travail").first()

    if not sircom:
        return False

    sites = [
        Site(nom="solidarites.gouv.fr", url="https://solidarites.gouv.fr",
             description="Portail des solidarités et de la santé", organisation_id=sircom.id),
        Site(nom="travail-emploi.gouv.fr", url="https://travail-emploi.gouv.fr",
             description="Portail du travail et de l'emploi", organisation_id=sircom.id),
        Site(nom="drees.solidarites-sante.gouv.fr", url="https://drees.solidarites-sante.gouv.fr",
             description="Direction de la recherche, des études, de l'évaluation et des statistiques",
             organisation_id=bcom_sante.id if bcom_sante else sircom.id),
        Site(nom="code.travail.gouv.fr", url="https://code.travail.gouv.fr",
             description="Code du travail numérique",
             organisation_id=bcom_travail.id if bcom_travail else sircom.id),
    ]
    db.session.add_all(sites)
    db.session.commit()
    return True
