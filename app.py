import streamlit as st
import json

# Charger les questions depuis data.json
with open("data.json", "r", encoding="utf-8") as file:
    questions = json.load(file)["questions"]

# Stockage des réponses de l'utilisateur
user_answers = {}

# Interface principale
st.title("Score de Maturité Numérique")

# Explication du modèle
st.markdown("""
Inspiré du Digital Maturity Model (DMM), ce modèle de maturité numérique évalue la maturité de votre organisation à travers plusieurs axes.
""")

# Questionnaire interactif
for question in questions:
    st.subheader(question["text"])
    options = list(question["choices"].keys())
    response = st.radio("", options, key=question["text"])
    user_answers[question["text"]] = question["choices"][response]

# Bouton pour soumettre
if st.button("Voir les résultats"):
    scores = {}
    for question in questions:
        axis = question["axis"]
        scores.setdefault(axis, []).append(user_answers[question["text"]])

    # Calcul de la moyenne pour chaque axe
    final_scores = {axis: sum(values) / len(values) for axis, values in scores.items()}

    st.subheader("Résultats")
    st.write("Voici votre score moyen par axe :")
    st.json(final_scores)

    # Visualisation des scores avec un graphique
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame.from_dict(final_scores, orient="index", columns=["Score"])
    df.plot(kind="bar", legend=False, color="royalblue")
    plt.xticks(rotation=45)
    plt.title("Score de Maturité par Axe")
    plt.ylabel("Score")
    st.pyplot(plt)
