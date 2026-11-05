"""Page 3 : Routage de tickets vers des catégories.

Starter Kit Apprenants - Brief 2 IA-TOS.
"""

import os
import requests
import streamlit as st
import pandas as pd

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Routage de tickets | Brief 2",
    page_icon="🧾",
    layout="wide",
)

st.title("Page 3 : Routage de tickets vers des catégories")
st.markdown("""
Cette page permet de router les tickets vers des catégories prédéfinies en utilisant un modèle de classification zero-shot DeBERTa-v3.
""")


# ==============================================================================
# TODO (Apprenants) : Implémenter la saisie textuelle et l'appel API
#
# Étapes suggérées :
# Saisie du ticket, sélection dynamique des catégories via st.multiselect, graphique st.bar_chart des probabilités.
# ==============================================================================

texte_saisi = st.text_area("Entrez le texte du ticket", height=150)
categories = st.multiselect("Sélectionnez les catégories", ["Banque / Paiement", "Ressources Humaines", "Informatique / VPN"], accept_new_options=True)



if st.button("Classer le ticket"):

    if texte_saisi:
        try:
            payload = {"ticket_text": texte_saisi, "categories": categories}
            resp = requests.post(f"{FASTAPI_URL}/classify-ticket", json=payload, timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                top_category = result.get("top_category")
                confidence = result.get("confidence")
                distribution = result.get("distribution")

                st.write("Visualisation graphique des scores par catégorie :")  
                st.metric(label="Catégorie principale", value=top_category, delta=None)
                st.metric(label="Confiance", value=f"{confidence * 100:.2f}%", delta=None)

                score_en_pourcentage = [d["score"] * 100 for d in distribution]
                df_distribution = pd.DataFrame(distribution)
                df_distribution["score_en_pourcentage"] = df_distribution["score"] * 100
                df_distribution = df_distribution.sort_values(by="score_en_pourcentage", ascending=False)
                st.bar_chart(df_distribution, x="category", y="score_en_pourcentage", x_label="Catégorie", y_label="Score de confiance", sort=False)
            else:
                st.error(f"Erreur API : Statut {resp.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'appel API")
    else:
        st.warning("Veuillez entrer un texte à analyser.")