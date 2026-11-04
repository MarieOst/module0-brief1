"""Page 2 : Analyseur de Sentiment (Baseline Lexicale NLTK VADER M0).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os
import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Analyse de Sentiment | Brief 1",
    page_icon="💬",
    layout="wide",
)

st.title("Page 2 : Analyseur de Sentiment des Retours Clients")
st.markdown("""
Cette page interroge le microservice NLP d'analyse de polarite base sur la methode lexicale 
**NLTK VADER** (`SentimentIntensityAnalyzer`).
""")

st.info("""
**Note d'architecture pedagogique (M0)** : Cette approche par dictionnaire lexical constitue notre 
baseline de depart. Elle sera confrontee puis remplacee dans les modules suivants par des modeles 
de Transformers pre-entraines en francais (**CamemBERT / RoBERTa**) et du Fine-Tuning LoRA (PEFT).
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter la saisie textuelle et l'appel API
#
# Étapes suggérées :
# 1. Proposer une zone de saisie texte avec st.text_area().
# 2. Optionnel : Proposer des boutons de texte d'exemples (positif, négatif, neutre).
# 3. Ajouter un bouton d'action avec st.button("Analyser la polarité").
# 4. Lors du clic :
#    a. Émettre un POST vers f"{FASTAPI_URL}/predict/sentiment" avec le payload JSON :
#       {"texte": texte_saisi}
#    b. Récupérer la réponse JSON (SentimentPredictResponse) contenant :
#       - label (str : 'Positif', 'Neutre', 'Negatif')
#       - compound (float entre -1.0 et 1.0)
#       - details (dict avec 'pos', 'neu', 'neg')
#       - method (str)
#    c. Restituer le résultat avec des composants visuels adaptés (st.metric, st.progress, etc.).
# ==============================================================================

texte_saisi = st.text_area("Entrez le texte à analyser", height=150)
analyse_button = st.button("Analyser la polarité")

if analyse_button:
    if texte_saisi:
        try:
            payload = {"texte": texte_saisi}
            resp = requests.post(f"{FASTAPI_URL}/predict/sentiment", json=payload, timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                label = result.get("label")
                compound = result.get("compound")
                type_modele = result.get("type_modele")

                st.metric(label="Polarité", value=f"{compound:.2f}", delta=None)
                st.badge(f"Label : {label}", color="green" if label == "Positif" else "orange" if label == "Neutre" else "red")
                st.info(f"Méthode : {type_modele}")
            else:
                st.error(f"Erreur API : Statut {resp.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'appel API")
    else:
        st.warning("Veuillez entrer un texte à analyser.")