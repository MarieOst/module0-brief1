"""Page 1 : Formulaire de Scoring de Credit (Baseline Regression Lineaire M0).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os
import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Scoring Credit | Brief 1",
    page_icon="💳",
    layout="wide",
)

st.title("Page 1 : Formulaire Predictif de Scoring de Credit")
st.markdown("""
Cette page interroge le microservice de scoring de credit base sur une **Regression Lineaire Scikit-Learn** 
entrainee sur les 3 variables financieres neutres du dossier (`montant_demande`, `duree_mois`, `revenu_mensuel`).
""")

st.info("""
**Note d'architecture pedagogique (M0)** : Ce modele est restreint a 3 variables neutres. 
Le dataset complet contient des variables demographiques et contextuelles qui serviront au **Module 2** 
pour realiser l'audit d'equite algorithmique (Disparate Impact), l'anonymisation RGPD et la mitigation des biais.
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter le formulaire Streamlit et l'appel API
#
# Étapes suggérées :
# 1. Créer un formulaire avec st.form("form_credit").
# 2. Ajouter les champs de saisie :
#    - montant_demande (st.number_input, ex: 1000 à 50000 €)
#    - duree_mois (st.slider, ex: 6 à 84 mois)
#    - revenu_mensuel (st.number_input, ex: 500 à 20000 €)
#    - bouton de soumission (st.form_submit_button)
# 3. Lors de la soumission du formulaire :
#    a. Émettre un POST vers f"{FASTAPI_URL}/predict/credit" avec le payload JSON :
#       {"montant_demande": float, "duree_mois": int, "revenu_mensuel": float}
#    b. Récupérer la réponse JSON (CreditPredictResponse) contenant :
#       - score (float entre 300 et 850)
#       - decision (str : 'Favorable', 'Ajourne / Examen Approfondi', 'Defavorable')
#       - seuil_recommande (float)
#       - model_version (str)
#    c. Restituer visuellement le score (ex: st.metric, jauge de progression, couleur de badge).
# ==============================================================================

st.info("A vous de jouer ! Implementez le formulaire et l'affichage des predictions de credit.")
