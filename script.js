// initialisation des données directement dans le script pour plus de simplicité
const jsonData = 
{
  "questions": [
      
      {
          "text": "Quelle est la portée de la vision stratégique que vous avez pour vos sites ? ",
          "choices": {
              "1 an": 1,
              "3 ans": 2,
              "5 ans": 3,
              "10 ans": 4
          },
          "theme": "Portée de la vision produit",
          "axis": "Stratégie"
      },
      {
          "text": "Comment la vision web est-elle partagée ?",
          "choices": {
              "Elle n'est pas partagée": 1,
              "De manière informelle, en fonction des besoins": 2,
              "De manière formelle et régulière": 3,
              "C'est un aspect abordé dans toute communication": 4
          },
          "theme": "Partage de la vision produit",
          "axis": "Stratégie"
      },
      {
          "text": "Quel phrase décrit le mieux la situation actuelle ?",
          "choices": {
              "On gère les sites au jour le jour": 1,
              "On rationalise l'usage des outils et des ressources": 2,
              "On standardise les processus et les applications": 3,
              "On optimise nos processus en continu": 4
          },
          "theme": "Tendance",
          "axis": "Stratégie"
      },
      {
          "text": "Comment les besoins des usagers sont pris en compte ? ",
          "choices": {
              "Pas de prise en compte": 1,
              "Tests ou études ad-hoc": 2,
              "Tests ou études systématiques": 3,
              "Les usagers sont intégrés au processus de design": 4
          },
          "theme": "Prise en compte des usagers",
          "axis": "Stratégie"
      },
      {
          "text": "Comment gérez-vous les tests utilisateurs pour vos produits ?",
          "choices": {
              "Pas de tests utilisateurs": 1,
              "Tests utilisateurs ponctuels, informels": 2,
              "Tests utilisateurs réguliers,  formels": 3,
              "Tests utilisateurs intégrés au design": 4
          },
          "theme": "Tests utilisateurs",
          "axis": "Stratégie"
      },
      {
          "text": "Quels contenus et services proposez-vous principalement ? ",
          "choices": {
              "Des contenus d'information et d'actualité": 1,
              "Des contenus serviciels": 2,
              "Des services en ligne, indépendants": 3,
              "Des services unifiés": 4
          },
          "theme": "Positionnement",
          "axis": "Stratégie"
      },
      {
          "text": "Quelle est la principale mesure de l'activité de vos services",
          "choices": {
              "La production de contenus et le nombre de demandes prises en charge (plus c'est mieux)": 1,
              "La qualité des contenus produits et la valeur ajoutée des évolutions": 2,
              "La qualité du service rendu par les contenus et les fonctions du site": 3,
              "La qualité de service": 4
          },
          "theme": "Mesure de l'activité",
          "axis": "Stratégie"
      },
      {
          "text": "Comment mesurez-vous la satisfaction des utilisateurs de vos produits ?",
          "choices": {
              "Pas de mesure": 1,
              "Analyse statistiques ou enquêtes basiques": 2,
              "Analyses de satisfaction dédiés et études pontuelles": 3,
              "Evaluation et adaptation continues": 4
          },
          "theme": "Mesure de la satisfaction",
          "axis": "Stratégie"
      },
      {
          "text": "Quelle est l'étendue des services omnicanaux ?",
          "choices": {
              "Les services sont uniquement disponibles sur le web ": 1,
              "Le service varie selon le canal utilisé. Préférences utilisateur non pris en compte": 2,
              "L'éxpérience est cohérente sur tous les canaux. Lien avec les représentations physiques": 3,
              "L'expérience est personnalisée, cohérente et intégrée sur tous les canaux, y compris les assistants vocaux et les chatbots": 4
          },
          "theme": "Omnicanal",
          "axis": "Stratégie"
      },
      {
          "text": "Avec quels outils sont gérés la relation citoyen",
          "choices": {
              "Outils dédiés à chaque canal": 1,
              "CRM dédié pour chaque canal, connectable. ": 2,
              "CRM unifié multicanal ": 3,
              "CRM intégré au SI métier": 4
          },
          "theme": "Marketing",
          "axis": "Stratégie"
      },
      {
        "text": "Existe-il un cycle de vie documentaire défini ? ",
        "choices": {
            "Non, aucun (culture orale)": 1,
            "Oui, mais pas pour tous les types de contenus": 2,
            "Oui, mais sans automatisation (pas de workflow lié)": 3,
            "Oui, intégré au workflow de production de contenus": 4
        },
        "theme": "Cycle de vie documentaire",
        "axis": "Processus"
    },
    {
        "text": "Existe-il un workflow éditorial défini ? ",
        "choices": {
            "Non, aucun (ou hors outil)": 1,
            "Oui, mais pas pour toutes les publications": 2,
            "Oui, mais sans automatisation (pas de notification mail ou de déclencheur lié au cycle de vie)": 3,
            "Oui, intégré au cycle de vie documentaire": 4
        },
        "theme": "Workflow éditorial",
        "axis": "Processus"
    },
    {
        "text": "Quel est l'outil principal utilisé pour créer et valider les contenus ?",
        "choices": {
            "Dans des outils bureautiques principalement": 1,
            "Dans des outils bureautiques liés au CMS (notifications, etc…)": 2,
            "Dans le CMS, via une édition WYSIWYG": 3,
            "Dans le CMS, via une édition WYSIWYM (what you MEAN)": 4
        },
        "theme": "Rédaction",
        "axis": "Processus"
    },
    {
        "text": "Comment ou par qui sont coordonnées les actions ? ",
        "choices": {
            "Pilotage partagé de manière informelle entre plusieurs équipes ou personnes": 1,
            "Pilotage partagé de manière formelle entre plusieurs équipes ou personnes": 2,
            "Coordination décentralisée sur des rôles identifiés (product owner / resp. éditorial)": 3,
            "Coordination centralisée (rôles clé au sein de la même équipe)": 4
        },
        "theme": "Pilotage",
        "axis": "Processus"
    },
    {
        "text": "Quel est le niveau de culture numérique des collaborateurs du service ? ",
        "choices": {
            "Le numérique est encore perçu comme une spécialité. L'utilisation des outils est subie. ": 1,
            "Le numérique est perçu comme partie intégrante du métier, mais il reste à progresser pour beaucoup": 2,
            "La majorité des agents sont à l'aise avec les outils et processus": 3,
            "Le numérique fait partie de l'ADN de l'organisation. ": 4
        },
        "theme": "Culture",
        "axis": "Processus"
    },
    {
        "text": "Comment le numérique est géré au recrutement et au long de la carrière ? ",
        "choices": {
            "Cest un élément qui doit figurer dans la fiche de poste pour être exigé": 1,
            "Compétence souhaitée lors du recrutement. Accompagnement RH sur base de volontariat": 2,
            "Compétence exigée au recrutement. Accompagnement soutenu en interne si besoin. ": 3,
            "Compétence de base intégrée à tout processus RH. ": 4
        },
        "theme": "Ressources humaines",
        "axis": "Processus"
    },
      {
        "text": "L'outil de production des sites (Drupal) est perçu comme ?",
        "choices": {
            "Un outil de publication de pages web": 1,
            "Un outil de management de contenus web (séparés)": 2,
            "Un outil de management de corpus (contenus reliés)": 3,
            "Une application métier dédiée à la gestion de contenus": 4
        },
        "theme": "Outil de travail",
        "axis": "Contenus"
    },
    {
        "text": "De quelle manière les contenus sont structurés dans le CMS ?",
        "choices": {
            "Pas de structure spécifique ou partagée": 1,
            "Structure proposée par charte éditoriale (hors outil)": 2,
            "Plan de classement intégré à l'outil (non centralisé)": 3,
            "Plan de classement intégré à l'outil (centralisé)": 4
        },
        "theme": "Structure des contenus",
        "axis": "Contenus"
    },
    {
        "text": "Quelle est le niveau de \"dette\" éditoriale (contenus, fichiers, URLs…)",
        "choices": {
            "Très mportant, pas totalement chiffré": 1,
            "Important et chiffré, en réduction": 2,
            "Faible et mesuré": 3,
            "Inexistant (surveillance constante)": 4
        },
        "theme": "Corpus",
        "axis": "Contenus"
    },
    {
        "text": "Comment est géré le corpus iconographique ? ",
        "choices": {
            "Gestion manuelle et individuelle par chaque agent": 1,
            "Gestion centralisée dans une bibliothèque partagée (dédiée icono)": 2,
            "Bibliothèque icono intgrée avec le CMS": 3,
            "Bibliothèque commune pour icono et documentaire, intégrée au CMS": 4
        },
        "theme": "Iconographie",
        "axis": "Contenus"
    },
    {
        "text": "Comment est géré le corpus de fichiers",
        "choices": {
            "Gestion manuelle et individuelle par chaque agent": 1,
            "Gestion individuelle par chaque agent dans un DAM connecté au CMS": 2,
            "Gestion centralisée dans un DAM connecté au CMS": 3,
            "Gestion externalisée dans un DAM entreprise, connecté au CMS": 4
        },
        "theme": "Fichiers",
        "axis": "Contenus"
    },
      {
          "text": "Comment sont gérés les marqueurs sur vos sites (statistiques, campagnes)",
          "choices": {
              "Il n'y a pas de marqueurs": 1,
              "Ils sont ajoutés manuellement par les équipes techniques": 2,
              "Ils sont ajoutés via un TMS par les équipes métier": 3,
              "Ils sont ajoutés automatiquement (lien depuis outil de gestion de campagne)": 4
          },
          "theme": "Marketing",
          "axis": "Technique"
      },
      {
          "text": "Comment est percu l'enjeu autour des moteurs de recherche internes ?",
          "choices": {
              "C'est un rôle délégué aux techniciens": 1,
              "Les règles sont déléguées à la technique, mais le corpus est optimisé par les équipes éditoriales": 2,
              "Le moteur de recherche est surveillé par la technique, mais piloté par les équipes éditoriales": 3,
              "Le moteur de recherche est enrichi par les équipes métier": 4
          },
          "theme": "Moteur de recherche",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau d'outillage du CMS pour les administrateurs",
          "choices": {
              "Pas d'outils autre que les outils de base": 1,
              "Quelques fonctionnalités d'administrations développées spécifiquement (réactif)": 2,
              "Fonctions d'administration avancées (monitoring, réactif)": 3,
              "Fonctions d'adminustrations avancées et proactives": 4
          },
          "theme": "Administration",
          "axis": "Technique"
      },
      {
          "text": "Comment sont gérées les sites web dans le temps ? ",
          "choices": {
              "Des refontes récurentes intercalées de TMA corrective": 1,
              "Des refontes plus espacées, soutenues par de la TMA évolutive": 2,
              "Mis en place d'une évolution continue, mais encore avec une vision \"site\"": 3,
              "Evolution continue avec une vision \"service\"": 4
          },
          "theme": "Gestion des évolutions",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de dette technique ? ",
          "choices": {
              "Très mportant, pas totalement chiffré": 1,
              "Important et chiffré, en réduction": 2,
              "Faible et mesuré": 3,
              "Inexistant (surveillance constante)": 4
          },
          "theme": "Dette technique",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau d'intégration du SI communication au SI global ? ",
          "choices": {
              "Aucun. Intégration rudimentaire": 1,
              "Des API permettent d'échanger des données publiques": 2,
              "un DAM permet de centraliser les données de l'organisation": 3,
              "Toutes les ressources sont centralisées dans le SI Global": 4
          },
          "theme": "Infrastructure",
          "axis": "Technique"
      },
      {
          "text": "Quel est le type d'hébergement pour vos sites internet ? ",
          "choices": {
              "Hébergement dédié, sur base de machines virtuelles": 1,
              "Hébergement dédié, sur base d'images": 2,
              "Hébergement cloud de confiance, sur base d'image": 3,
              "Hébergement interne ou cloud de confiance": 4
          },
          "theme": "Cloud",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de maturité sur l'accessibilité ? ",
          "choices": {
              "On commence à s'emparer du sujet, on mesure. On doit être vers 50%": 1,
              "On a un processus de mesure, on améliore au fil de l'eau. On vise 75% ": 2,
              "On intègre le sujet dès le design, on règle la dette. On vise 90%": 3,
              "Evaluation et amélioration continue. On vise le 100%": 4
          },
          "theme": "Accessibilité",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de maturité sur la sécurité ? ",
          "choices": {
              "On commence à s'emparer du sujet, on mesure. On doit être vers 50%": 1,
              "On a un processus de mesure, on améliore au fil de l'eau. On vise 75% ": 2,
              "On intègre le sujet dès le design, on règle la dette. On vise 90%": 3,
              "Evaluation et amélioration continue. On vise le 100%": 4
          },
          "theme": "Sécurité",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de maturité sur le RGPD ? ",
          "choices": {
              "On commence à s'emparer du sujet, on mesure. On doit être vers 50%": 1,
              "On a un processus de mesure, on améliore au fil de l'eau. On vise 75% ": 2,
              "On intègre le sujet dès le design, on règle la dette. On vise 90%": 3,
              "Evaluation et amélioration continue. On vise le 100%": 4
          },
          "theme": "RGPD",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de maturité sur l'éco-conception ? ",
          "choices": {
              "On commence à s'emparer du sujet, on mesure. On doit être vers 50%": 1,
              "On a un processus de mesure, on améliore au fil de l'eau. On vise 75% ": 2,
              "On intègre le sujet dès le design, on règle la dette. On vise 90%": 3,
              "Evaluation et amélioration continue. On vise le 100%": 4
          },
          "theme": "Eco-conception",
          "axis": "Technique"
      },
      {
          "text": "Quel est le niveau de maturité sur le DSFR ? ",
          "choices": {
              "On commence à s'emparer du sujet, on mesure. On doit être vers 50%": 1,
              "On a un processus de mesure, on améliore au fil de l'eau. On vise 75% ": 2,
              "On intègre le sujet dès le design, on règle la dette. On vise 90%": 3,
              "Evaluation et amélioration continue. On vise le 100%": 4
          },
          "theme": "DSFR",
          "axis": "Technique"
      }
  ]
}
  let currentQuestionIndex = 0;

//écoute le lancement du questionnaire

  document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("startBtn");
    if (startBtn) {
      startBtn.addEventListener("click", () => {
        window.location.href = "questions.html";
      });
    }
  });
  
 //charge la page de résultats 
  function goToResults() {
    window.location.href = "results.html";
  }
  
  // Affiche les questions
  function displayQuestion(questionData) {
    const questionContainer = document.getElementById("questionsContainer");
  
    // Vider le conteneur de questions
    questionContainer.innerHTML = '';
    const axisTitle = document.createElement("span");
    axisTitle.className = "badge badge-primary";
    axisTitle.textContent = "Axe : " + questionData.axis;
    questionContainer.appendChild(axisTitle);
  
    const themeTitle = document.createElement("span");
    themeTitle.className = "badge badge-secondary";
    themeTitle.textContent = "Thème : " + questionData.theme;
    questionContainer.appendChild(themeTitle);


    const titlesContainer = document.createElement("p");
    titlesContainer.appendChild(axisTitle);
    titlesContainer.appendChild(themeTitle);
  
    const choicesFieldset = document.createElement("fieldset");
    const choicesLegend = document.createElement("legend");
    choicesLegend.textContent = questionData.text;
    choicesFieldset.appendChild(choicesLegend);
  
    const choicesList = document.createElement("ul");
    choicesList.classList.add("list-unstyled");
  
    let choiceIndex = 0;
    for (const choiceText in questionData.choices) {
      const listItem = document.createElement("li");
  
      const choiceInput = document.createElement("input");
      choiceInput.classList.add("form-check-input");
      choiceInput.type = "radio";
      choiceInput.name = "choice";
      choiceInput.value = questionData.choices[choiceText];
      choiceInput.id = `question${currentQuestionIndex}_choice${choiceIndex}`;
  
      const choiceLabel = document.createElement("label");
      choiceLabel.classList.add("form-check", "mb-3");
      choiceLabel.textContent = choiceText;
      choiceLabel.setAttribute("for", `question${currentQuestionIndex}_choice${choiceIndex}`);
  
      listItem.appendChild(choiceInput);
      listItem.appendChild(choiceLabel);
      choicesList.appendChild(listItem);
  
      choiceIndex++;
    }
    questionContainer.appendChild(titlesContainer);

    const progressBarContainer = document.createElement("div");
    progressBarContainer.className = "progress my-3";
    
    const progressBar = document.createElement("div");
    progressBar.className = "progress-bar";
    progressBar.setAttribute("role", "progressbar");
    progressBar.style.width = `${((currentQuestionIndex) / jsonData.questions.length) * 77}%`;
    progressBar.setAttribute("aria-valuenow", currentQuestionIndex );
    progressBar.setAttribute("aria-valuemin", "0");
    progressBar.setAttribute("aria-valuemax", jsonData.questions.length);
    
    progressBarContainer.appendChild(progressBar);
    questionContainer.appendChild(progressBarContainer);


    choicesFieldset.appendChild(choicesList);
    questionsContainer.appendChild(choicesFieldset);

    const questionKey = `${questionData.axis}-${questionData.theme}`;
    if (userAnswers[questionKey] && userAnswers[questionKey].includes(parseInt(choiceInput.value, 10))) {
      choiceInput.checked = true;
    }
    

  }
  
  
  document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("questionsContainer")) {
      displayQuestion(jsonData.questions[currentQuestionIndex]);
    }

    const backBtn = document.getElementById("backBtn");
    if (backBtn) {
      backBtn.addEventListener("click", handlePreviousQuestion);
    }

  });
  
  // Stocke les réponses utilisateur
  const userAnswers = {};

  // enregistre les réponses
  function saveUserAnswer() {
    const choices = document.querySelectorAll('input[name="choice"]');
    let userChoice = null;
  
    choices.forEach((choice) => {
      if (choice.checked) {
        userChoice = parseInt(choice.value, 10);
      }
    });
  
    if (userChoice !== null) {
      const questionData = jsonData.questions[currentQuestionIndex];
      const questionKey = `${questionData.axis}-${questionData.theme}`;
      
      if (!userAnswers[questionKey]) {
        userAnswers[questionKey] = [];
      }
      
      userAnswers[questionKey].push(userChoice);
    }
  }
// aller à la prochaine question
function handleNextQuestion() {
    saveUserAnswer();
    currentQuestionIndex++;
  
    if (currentQuestionIndex < jsonData.questions.length) {
      displayQuestion(jsonData.questions[currentQuestionIndex]);
    } else {
      calculateResults();
      goToResults();
    }
  }
  
//calculer les résultats
function calculateResults() {
    const themeResults = {};
    const axisResults = {};
  
    for (const questionKey in userAnswers) {
      const [axis, theme] = questionKey.split("-");
      const answerList = userAnswers[questionKey];
      const averageScore = answerList.reduce((a, b) => a + b) / answerList.length;
  
      themeResults[theme] = averageScore;
  
      if (!axisResults[axis]) {
        axisResults[axis] = [];
      }
  
      axisResults[axis].push(averageScore);
    }
  
    for (const axis in axisResults) {
      const themeList = axisResults[axis];
      const averageScore = themeList.reduce((a, b) => a + b) / themeList.length;
      axisResults[axis] = averageScore;
    }
  
    sessionStorage.setItem("themeResults", JSON.stringify(themeResults));
    sessionStorage.setItem("axisResults", JSON.stringify(axisResults));
  }
  
  //Paramètres du graphique de résultats
  let chart = null;

function createChart(labels, data) {
  const ctx = document.getElementById("chart").getContext("2d");

  if (chart) {
    chart.destroy();
  }

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Score",
          data: data,
          backgroundColor: [
            'rgb(181, 208, 235)', // Bleu pastel
            'rgb(255, 179, 186)', // Rose pastel
            'rgb(218, 247, 166)', // Vert clair pastel
            'rgb(255, 229, 173)', // Jaune pastel
            'rgb(243, 156, 202)', // Rose bonbon pastel
            'rgb(173, 216, 230)', // Bleu clair pastel
            'rgb(246, 199, 255)', // Violet pastel
            'rgb(174, 198, 207)', // Bleu-gris pastel
            'rgb(255, 218, 193)', // Orange pastel
            'rgb(199, 244, 100)', // Vert pomme pastel
            'rgb(255, 253, 208)', // Jaune pâle pastel
            'rgb(230, 190, 255)', // Mauve pastel
          ],
          borderColor: [
            'rgb(181, 208, 235)', // Bleu pastel
            'rgb(255, 179, 186)', // Rose pastel
            'rgb(218, 247, 166)', // Vert clair pastel
            'rgb(255, 229, 173)', // Jaune pastel
            'rgb(243, 156, 202)', // Rose bonbon pastel
            'rgb(173, 216, 230)', // Bleu clair pastel
            'rgb(246, 199, 255)', // Violet pastel
            'rgb(174, 198, 207)', // Bleu-gris pastel
            'rgb(255, 218, 193)', // Orange pastel
            'rgb(199, 244, 100)', // Vert pomme pastel
            'rgb(255, 253, 208)', // Jaune pâle pastel
            'rgb(230, 190, 255)', // Mauve pastel
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          max: 4,
          ticks: {
            stepSize: 1, // Ajoutez l'option stepSize pour ne pas afficher les demi-points
          },
        },
      },
    },
  });
}

// Fonction d'affichage des résultats
function displayResults() {
  const themeResults = JSON.parse(sessionStorage.getItem("themeResults"));
  const axisResults = JSON.parse(sessionStorage.getItem("axisResults"));

  createChart(Object.keys(axisResults), Object.values(axisResults));

  const themeButtonsContainer = document.getElementById("themeButtons");

  // Crée un objet pour stocker les thèmes par axe
  const themesByAxis = {};

  // Parcours toutes les questions pour regrouper les thèmes par axe
  jsonData.questions.forEach((question) => {
    const { theme, axis } = question;

    if (!themesByAxis[axis]) {
      themesByAxis[axis] = [];
    }

    if (!themesByAxis[axis].includes(theme)) {
      themesByAxis[axis].push(theme);
    }
  });

  // Crée des boutons pour chaque axe
  for (const axis in themesByAxis) {
    const button = document.createElement("button");
    button.textContent = `Voir le détail de ${axis}`;
    button.classList.add("btn", "btn-outline-secondary", "btn-sm")
    button.addEventListener("click", () => {
      const themes = themesByAxis[axis];
      const themeScores = themes.map((theme) => themeResults[theme]);
      createChart(themes, themeScores);
      document.getElementById("globalViewBtn").style.display = "block";
    });
    themeButtonsContainer.appendChild(button);
  }

  document.getElementById("globalViewBtn").addEventListener("click", () => {
    createChart(Object.keys(axisResults), Object.values(axisResults));
    document.getElementById("globalViewBtn").style.display = "none";
  });
}

  
  
  document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("resultsContainer")) {
      displayResults();
    }
  });
  
  function handlePreviousQuestion() {
    saveUserAnswer();
    currentQuestionIndex--;
  
    if (currentQuestionIndex >= 0) {
      displayQuestion(jsonData.questions[currentQuestionIndex]);
    } else {
      window.location.href = "index.html";
    }
  }
  
  