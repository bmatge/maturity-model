import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Charger les questions depuis data.json
with open("data.json", "r", encoding="utf-8") as file:
    questions = json.load(file)["questions"]

# Stockage des réponses de l'utilisateur
user_answers = {}

# Interface principale
st.title("Score de Maturité Numérique")

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

    # 📊 Visualisation avec Streamlit
    df = pd.DataFrame.from_dict(final_scores, orient="index", columns=["Score"])

    # Utiliser Streamlit pour l'affichage du graphique
    st.bar_chart(df)
