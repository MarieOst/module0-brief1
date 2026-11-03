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

st.info("A vous de jouer ! Implementez l'analyseur de sentiment et l'affichage des metriques NLP.")
