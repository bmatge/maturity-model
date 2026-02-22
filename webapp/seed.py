"""
Seed du référentiel v2 — 44 capacités × 4 niveaux = 176 critères.
Exécuté automatiquement au premier lancement si la DB est vide.
"""

from models import (
    db, ReferentielVersion, Dimension, Capacite, NiveauCritere, Entite, Campagne
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
