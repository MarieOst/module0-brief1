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

colonne_formulaire, colonne_resultats = st.columns(2)

with colonne_formulaire:
    with st.form("form_credit"):
        st.write("A compléter")
        montant_demande = st.number_input("Montant sollicité", min_value=1000, max_value=50000, value=10000, step=500)
        duree_mois = st.slider("Durée du remboursement", 6, 84, 36)
        revenu_mensuel = st.number_input("Revenu mensuel net (€)", min_value=500, max_value=20000, value=2000, step=100)
        submit_button = st.form_submit_button("Soumettre")

if submit_button:
    try:
        payload = {
            "montant_demande": montant_demande,
            "duree_mois": duree_mois,
            "revenu_mensuel": revenu_mensuel
        }
        resp = requests.post(f"{FASTAPI_URL}/predict/credit", json=payload, timeout=5)
        with colonne_resultats:
            if resp.status_code == 200:
                result = resp.json()
                score = result.get("score")
                decision = result.get("decision")
                #seuil_recommande = result.get("seuil_recommande")
                type_modele = result.get("type_modele")

                st.metric(label="Score de Credit", value=f"{score:.2f}", delta=None)
                ##st.info(f"Seuil Recommande : {seuil_recommande:.2f}")
                st.badge(f"Decision : {decision}", color="green" if decision == "Favorable" else "orange" if decision == "Ajourne / Examen Approfondi" else "red")
                st.info(f"Version du Modele : {type_modele}")
                
            else:
                st.error(f"Erreur API : Statut {resp.status_code}")
    except Exception as e:
        with colonne_resultats:
            st.error(f"Erreur lors de l'appel API")