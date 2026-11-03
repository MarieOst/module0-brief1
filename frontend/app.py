"""Application Streamlit multi-pages - Page d'accueil & Page 0 (Chatbot LangGraph).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os
import requests
import streamlit as st

# URL du backend FastAPI (injectable via variable d'environnement)
FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Plateforme IA-TOS | Brief 1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar globale avec statut de l'API
with st.sidebar:
    st.title("Plateforme IA-TOS")
    st.caption("Module 0 : Socle Applicatif & Microservices")
    st.divider()

    # Verification de l'etat de l'API FastAPI
    try:
        resp = requests.get(f"{FASTAPI_URL}/health", timeout=2)
        if resp.status_code == 200:
            st.success("API Backend : En ligne")
        else:
            st.warning(f"API Backend : Statut {resp.status_code}")
    except Exception:
        st.error("API Backend : Hors ligne (Vérifiez le port 8000)")

    st.markdown("""
    **Pages disponibles :**
    - **Page 0** : Chatbot Agentique (LangGraph)
    - **Page 1** : Scoring Credit (Regression Lineaire)
    - **Page 2** : Analyse de Sentiment (NLTK)
    """)
    st.divider()
    st.caption("Projet OPCO Atlas - Simplon & Atos 2026")

# En-tete principal
st.title("Page 0 : Assistant Conversationnel Agentique")
st.markdown("""
Bienvenue sur la plateforme unifiee **IA-TOS**. Cet agent conversationnel est orchestre avec **LangGraph** 
et connecte au LLM local **Qwen 2.5** via **Ollama**. Il possede un outil deterministe de calcul arithmetique (`calculer`).
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter l'interface de chat conversationnelle
# 
# Étapes suggérées :
# 1. Initialiser st.session_state["messages"] s'il n'existe pas encore.
# 2. Afficher les messages existants de st.session_state["messages"] avec st.chat_message().
# 3. Récupérer la saisie utilisateur avec st.chat_input().
# 4. Lors de l'envoi :
#    a. Ajouter le message utilisateur dans st.session_state["messages"] et l'afficher.
#    b. Préparer l'historique et faire une requête HTTP POST vers f"{FASTAPI_URL}/chat"
#       avec le payload : {"message": user_prompt, "history": history_payload}
#    c. Récupérer la réponse JSON (ChatResponse) :
#       - response (str) : texte de réponse
#       - tool_called (bool) : indique si l'outil a été utilisé
#       - tool_results (list) : traces des outils
#    d. Afficher la réponse dans le chat assistant et ajouter au session_state.
#    e. Si tool_called est True, afficher un expander montrant les calculs effectués.
# ==============================================================================

st.info("A vous de jouer ! Implementez la logique de chat conversationnelle ci-dessous.")
