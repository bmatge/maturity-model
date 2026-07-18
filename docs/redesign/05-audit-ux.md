---
type: ux-audit
app: Maturité numérique (maturity-model)
project: maturity-model
date: 2026-07-18
personas: [camille-repondante, nadia-pilote, marc-sponsor, admin-occasionnel]
tags: [ux-audit, maturity-model]
---

# Audit UX — Maturité numérique (2026-07-18)

## Cadrage

**Objectif de l'app** : permettre aux équipes de com du ministère de s'auto-évaluer sur des
référentiels de maturité, aux pilotes d'organiser des campagnes semestrielles, et aux décideurs
de lire des restitutions — données auto-déclarées et justifiées.

**Personas évalués** (ordre d'arbitrage : **Camille > Nadia > Marc > Admin**) :
- **Camille, répondante** : chargée de com, à l'aise avec Word/Outlook, pas avec les outils riches. Répond 1–2×/an. Craint le jargon et de « mal répondre ».
- **Nadia, pilote** : cheffe de projet, veut de l'efficacité (lancer, suivre, relancer, restituer).
- **Marc, sponsor** : chef de service pressé, lit en réunion, veut des messages pas des chiffres bruts.
- **Admin occasionnel** : gère référentiels/comptes rarement.

**Méthode** : audit **statique (lecture de code) + pilotage HTTP** (curl, connexion réelle en tant
que Camille sur le serveur de démo `127.0.0.1:5050`, rendu des écrans questionnaire avec données
réelles). Pas de pilotage navigateur (Chrome occupé) — **une revue en navigation clavier/souris et
un test sur mobile réel restent recommandés** (voir Notes méthodologiques).

**Périmètre** : parcours répondant complet (Mes évaluations → Démarrer → Questionnaire → Vérifier →
Résultats), en-tête / switcher d'espaces / sidemenu, tableau de bord pilote, détail de campagne
(4 onglets), restitution lecteur. Écrans data lourds (dashboard campagne, comparer) survolés.

## Synthèse

**L'application est déjà d'un très bon niveau de soin rédactionnel** : vouvoiement cohérent, micro-copy
pédagogique, états vides tous traités, garde-fous explicites (anti-doublon, confirmation de suppression),
et surtout une vraie intention *progressive disclosure* (lecture simple + accordéon « vue experte »
sur les résultats, invitation qui pré-remplit tout pour éviter à Camille l'écran de configuration).
Le socle est sain — cet audit cherche les frictions résiduelles, pas à refonder.

**Camille** : parcours globalement rassurant et bien séquencé. **Un défaut grave subsiste** : le
questionnaire n'a **pas d'autosave** alors que le lien de sortie affirme « le brouillon est conservé ».
C'est précisément le risque n°1 de ce persona (perte de saisie = abandon). À corriger en priorité
absolue. Reste ensuite du jargon ponctuel (« portée C/D/P », « triplet », « évaluateur ») et un
écran « Démarrer » technique pour la répondante qui s'auto-lance.

**Nadia** : l'outillage est complet et dense, comme elle l'aime (onglets campagne, relances, périmètre,
heatmap). Peu de friction ; surtout de la cohérence de vocabulaire à resserrer (« entité » vs
« organisation »).

**Marc** : la restitution est remarquablement pensée pour lui (3 cartes-messages « point de départ /
chantier transverse / entité qui décroche », repères de couleur explicités). Peu à faire.

## Findings

### 🟢 Quick wins (< 1h, fort impact)

- **[Wording/Sécurité] Le lien « Quitter (le brouillon est conservé) » ment tant qu'il n'y a pas d'autosave** — *Camille (critique)*
  - **Symptôme** : en haut du questionnaire, `Quitter (le brouillon est conservé)` renvoie vers « Mes évaluations » par un simple lien, **sans soumettre le formulaire**. Or les réponses ne vivent que dans des `input` cachés côté client (aucun `fetch`/autosave, aucun `beforeunload`). Si Camille répond à 20 capacités puis clique « Quitter » (ou ferme l'onglet) sans avoir cliqué « Sauvegarder le brouillon », **tout est perdu** — et le libellé lui a promis le contraire.
  - **Pourquoi ça coince** : c'est le scénario de rupture le plus probable et le plus punitif pour ce persona (« interruption non pardonnée »). Le texte induit une fausse confiance qui aggrave la perte.
  - **Suggestion immédiate** (avant l'autosave, cf. refacto) : faire de « Quitter » un **bouton de sauvegarde** (`type=submit name=action value=save` qui poste puis redirige), et ajouter un avertissement `beforeunload` si des réponses non sauvées existent. Copy du bouton : `Enregistrer et quitter`. Tant que l'autosave n'est pas là, retirer la promesse « le brouillon est conservé » des liens qui ne sauvent pas.
  - **Effort** : S (le vrai autosave est en refacto ci-dessous, mais cette rustine supprime la perte de données tout de suite).

- **[Wording] « portée C/D/P » : un badge nu compréhensible seulement au survol** — *Camille (fort), Marc*
  - **Symptôme** : chaque capacité porte un badge `C`, `D` ou `P` dont le sens (« Centrale / Distribuée / Partagée ») n'est **que dans un `title=` au survol** — invisible au tactile et au premier coup d'œil. Camille voit une lettre sans clé.
  - **Pourquoi ça coince** : jargon d'expert (« portée C/D/P » est cité comme point de douleur explicite du persona), et l'info d'aide est inaccessible là où elle en a besoin (mobile, lecture rapide).
  - **Suggestion** : (a) au minimum, **une ligne de légende** en tête de questionnaire : « C = pilotée en central · D = du ressort de votre bureau · P = partagée ». (b) Mieux : afficher le mot en toutes lettres dans le badge (`Partagée`) plutôt que l'initiale. (c) La portée n'aide pas Camille à *noter* — envisager de la **masquer côté répondant** et de la réserver à la vue experte / au pilote.
  - **Effort** : S

- **[Wording] « triplet » — vocabulaire d'ingénieur** — *Camille*
  - **Symptôme** : « Vérifiez le triplet avant de commencer » (écran Démarrer) et « Chaque invitation pré-remplit le triplet référentiel + campagne + cible » (onglet Invitations).
  - **Pourquoi ça coince** : « triplet » ne veut rien dire pour une chargée de com ; ça sonne base de données.
  - **Suggestion** :
    - Démarrer → `Vérifiez que le référentiel et la cible sont les bons avant de commencer.`
    - Invitations → `Chaque invitation contient déjà le bon référentiel et la bonne organisation : le répondant n'a plus qu'à répondre.`
  - **Effort** : XS

- **[Wording] « Votre nom (évaluateur) »** — *Camille*
  - **Symptôme** : le champ nom est étiqueté avec le terme système entre parenthèses.
  - **Suggestion** : `Votre nom` (le mot « évaluateur » n'apporte rien à Camille ; le garder éventuellement en `fr-hint-text` : « la personne qui remplit cette évaluation »).
  - **Effort** : XS

- **[Cohérence] « entité » et « organisation » désignent la même chose au même endroit** — *Camille, Nadia, Marc*
  - **Symptôme** : le menu et les libellés disent **« Organisations »**, mais le texte courant dit **« entités »** : « relancez les **entités** en retard » (tableau de bord), carte latérale « X **entités** attendues », flash « Périmètre enregistré (X **entités** attendues) ».
  - **Pourquoi ça coince** : deux mots pour un concept = micro-doute à chaque lecture, surtout pour un non-initié qui se demande si « entité » ≠ « organisation ».
  - **Suggestion** : choisir **« organisation »** (déjà le terme du menu et le plus parlant) et le passer partout dans le texte visible. Réserver « entité » au code.
  - **Effort** : S

- **[Feedback] Sauvegarde du brouillon = retour brutal en haut de page** — *Camille*
  - **Symptôme** : « Sauvegarder le brouillon » poste puis **recharge la page en haut**. Sur le référentiel ComNum (44 capacités), Camille qui sauvegarde à la capacité 30 est renvoyée à la capacité 1.
  - **Suggestion** : après sauvegarde, revenir à l'ancre de la dernière capacité touchée (ou ne pas recharger — cf. autosave). À défaut, `redirect(... + "#dim-<dernière>")`.
  - **Effort** : S

### 🟡 Améliorations à planifier (1h–1j)

- **[Premier contact] L'écran « Démarrer » est technique pour la répondante qui s'auto-lance** — *Camille*
  - **Symptôme** : hors invitation, « Démarrer » présente un formulaire à 4 champs dont l'option référentiel se lit « *… — cible : organisation (3 niveaux)* » et une alerte sur la « protection anti-doublon ». C'est le vocabulaire de Nadia, pas de Camille.
  - **Pourquoi ça coince** : la plupart des Camille arrivent par un lien d'invitation (très bien pensé) et ne voient jamais cet écran — mais celle qui clique « Démarrer » dans le menu tombe dans l'espace de configuration du pilote.
  - **Suggestion** : simplifier l'option (`Référentiel Design — pour une organisation`), déplacer l'alerte anti-doublon en `hint` discret, et surtout **mettre en avant les invitations en attente** sur cet écran (« On vous a invité·e à : … » avec bouton Démarrer) pour que le self-start reste l'exception. Envisager de renommer l'entrée de menu `Démarrer` → `Démarrer une évaluation libre` pour signaler que c'est le chemin « sans invitation ».
  - **Effort** : M

- **[Wording] « niveau "Absent" » en résultat peut décourager** — *Camille*
  - **Symptôme** : le hero de résultats affiche « Score X / 3 — niveau "Absent" » quand la moyenne arrondit à 1. Formulé comme un verdict.
  - **Pourquoi ça coince** : l'exercice ne doit pas ressembler à un contrôle sanctionnant ; « Absent » en gros dans le bloc de tête est rude pour quelqu'un qui a joué le jeu honnêtement.
  - **Suggestion** : accompagner le niveau d'un cadrage orienté progression (« point de départ », « marge de progression forte ») plutôt qu'un simple label, et s'appuyer sur la carte « Prochaine étape » déjà présente (excellente) pour renvoyer vers l'action.
  - **Effort** : S

- **[Wording] « Heatmap » (anglicisme) sur le dashboard de campagne** — *Nadia (ok), Marc (si accompagné)*
  - **Symptôme** : titre « Heatmap — entités × capacités ».
  - **Pourquoi ça coince** : acceptable pour Nadia (experte data), mais si Marc regarde par-dessus son épaule, l'anglicisme + 44 colonnes = surcharge.
  - **Suggestion** : `Vue croisée organisations × capacités` (ou « Carte de chaleur »), et une phrase de lecture : « une case rouge = capacité faible pour cette organisation ». *Liberté DSFR assumée : ok tant que c'est explicité.*
  - **Effort** : S

### 🔴 Refactos UX (> 1j)

- **[Feedback/Sécurité] Autosave du questionnaire** — *Camille (structurant)*
  - **Constat** : toute la sécurité perçue du brouillon repose sur un clic manuel « Sauvegarder ». Pour un formulaire de 30–60 min fractionné, c'est le maillon faible.
  - **Suggestion** : autosave par capacité (un `fetch` POST au changement de niveau / justification, avec un indicateur discret « Enregistré ✓ » dans la barre de progression). Cela supprime d'un coup le finding critique n°1, la perte au « Quitter », et la perte de scroll. Décision produit à tracer en **ADR** (choix : autosave AJAX vs sauvegarde par section).
  - **Effort** : L

- **[Progressive disclosure] Fatigue sur les référentiels longs (ComNum, 44 capacités)** — *Camille*
  - **Constat** : le séquençage par dimension + la nav latérale avec compteurs par dimension est déjà une bonne base, mais rien n'invite à « faire une dimension puis souffler ». Risque de notation expéditive sur les dernières dimensions (biais documenté du persona).
  - **Suggestion** : proposer un mode « une dimension à la fois » (validation/enregistrement par section, sentiment d'avancer par paliers), avec récap de progression entre sections. À arbitrer avec l'autosave.
  - **Effort** : L

## Wording — suggestions concrètes

| Actuel | Persona impacté | Suggéré | Justification |
|--------|-----------------|---------|---------------|
| `Quitter (le brouillon est conservé)` | Camille | `Enregistrer et quitter` (+ le rendre réellement enregistrant) | Le brouillon n'est PAS conservé sans clic « Sauvegarder » : le libellé promet une sécurité inexistante |
| Badge `C` / `D` / `P` (sens au survol) | Camille, Marc | Légende visible : « C = pilotée en central · D = du ressort de votre bureau · P = partagée » (ou mot en toutes lettres) | « portée C/D/P » = jargon cité comme douleur ; l'aide au survol est invisible au tactile |
| `Vérifiez le triplet avant de commencer.` | Camille | `Vérifiez que le référentiel et la cible sont les bons avant de commencer.` | « triplet » = vocabulaire technique |
| `…pré-remplit le triplet référentiel + campagne + cible` | Camille/Nadia | `…contient déjà le bon référentiel et la bonne organisation` | idem |
| `Votre nom (évaluateur)` | Camille | `Votre nom` | « évaluateur » = terme système inutile |
| `… — cible : organisation (3 niveaux)` (option) | Camille | `Référentiel Design — pour une organisation` | « cible » + « X niveaux » = métadonnées de config |
| « relancez les **entités** en retard » / « X **entités** attendues » | Tous | « relancez les **organisations** en retard » / « X **organisations** attendues » | Cohérence avec le libellé de menu « Organisations » |
| `Score X / 3 — niveau "Absent"` | Camille | `Point de départ — Score X / 3` + renvoi vers « Prochaine étape » | Éviter le verdict décourageant sur de l'auto-déclaratif |
| `Heatmap — entités × capacités` | Nadia/Marc | `Vue croisée organisations × capacités` (+ phrase de lecture) | Anglicisme + besoin d'une clé de lecture |
| `Hors campagne — déclaration spontanée` | Camille | `Évaluation libre (hors campagne)` | « déclaration spontanée » est un peu administratif |

## Progressive disclosure — état des lieux

- **Mes évaluations (Camille)** : **exemplaire.** Trois zones nettes (« À compléter » avec invitations + brouillons, « Mes résultats »), badges d'état lisibles, échéances, reprise « là où vous vous êtes arrêté·e ». Rien à masquer, rien de superflu. C'est la référence à préserver.
- **Démarrer (Camille self-start)** : **trop exposé.** Expose la mécanique de configuration (référentiel/cible/campagne/anti-doublon) qui relève de Nadia. À simplifier et à reléguer derrière le chemin d'invitation (voir finding).
- **Questionnaire (Camille)** : bon équilibre — descriptions de niveaux **inline** (grande valeur), justification repliée par défaut (bien), callout « Un doute entre deux niveaux ? » (excellent garde-fou). Seul excès exposé au débutant : la **portée C/D/P**, qui n'aide pas à noter → candidate au masquage côté répondant.
- **Résultats (Camille)** : **modèle du genre.** Lecture simple (hero + « 3 choses à retenir ») au-dessus, « Vue détaillée (radar, scores, capacité par capacité) » dans un accordéon. C'est exactement la bonne stratification novice→expert.
- **Détail de campagne (Nadia)** : dense mais organisé en 4 onglets (Suivi / Périmètre / Invitations / Réglages) ; les actions destructives sont isolées dans « Réglages » avec `panel--danger` et modale de confirmation. Bon niveau d'exposition pour une experte.
- **Restitution (Marc)** : **priorisation du message réussie** — 3 cartes-messages avant tout chiffre, repères de couleur explicités, bloc « Fiabilité de la donnée » (participation + % justifié) qui adresse frontalement sa défiance sur l'auto-déclaratif. Le détail data reste accessible mais n'écrase pas le message.

## Recommandations prioritaires

1. **Supprimer le risque de perte de saisie** (finding critique) : autosave, ou a minima rendre « Quitter » réellement sauvegardant + `beforeunload`, et cesser de promettre « le brouillon est conservé » là où c'est faux. **C'est le seul point qui menace directement le taux de complétion de Camille — donc toute la chaîne de valeur.**
2. **Désamorcer le jargon côté répondant** : légende « portée », « triplet », « évaluateur », option référentiel — lot de quick wins XS/S à fort effet rassurant.
3. **Uniformiser « organisation »** dans tout le texte visible (retirer « entité » de l'UI).

## Bugs détectés au passage

- Aucun bug fonctionnel bloquant repéré en lecture de code / pilotage HTTP. Point de vigilance non-UX : `evaluation_results` recalcule la « prochaine étape » via une requête `Capacite.query.filter_by(numero=…).join(Dimension)...first()` qui suppose l'unicité du `numero` par référentiel — à vérifier si des numéros de capacité se répètent entre dimensions (risque de mauvaise capacité citée). À confirmer hors de cet audit UX.

## Notes méthodologiques

- **Audit statique + HTTP**, sans pilotage navigateur : le rendu (wording, structure, hiérarchie, parcours) a été vérifié sur le serveur de démo réel connecté en tant que Camille, mais **le comportement d'interaction fine et le rendu mobile n'ont pas été observés visuellement**. À compléter par :
  - Un **test sur mobile réel** du questionnaire (tactile) : valider notamment l'inaccessibilité du `title=` de la portée et l'ergonomie du `level-picker` au doigt.
  - Un **test des 5 secondes** sur « Mes évaluations » et sur « Démarrer » avec 2–3 chargé·es de com hors équipe projet.
  - Un **test de reprise** : quitter le questionnaire à mi-parcours par différents chemins (lien « Quitter », fermeture d'onglet, bouton retour) et mesurer la perte réelle — pour chiffrer l'urgence du finding critique.
- **Non couvert en profondeur** : écrans `comparer`, `plan_action`, `exporter`, `users`, `referentiel_import` (espace admin/pilote avancé) — à auditer dans une passe dédiée Nadia/Admin si besoin.
