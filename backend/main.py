"""Point d'entree principal de l'API FastAPI - Starter Kit Apprenants.

Ce fichier est le coeur de votre mission pour le backend de la plateforme IA-TOS.
Vous devez completer les routes ci-dessous en vous appuyant sur :
- Le package metier : iatos_core (agents, scoring, sentiment, logger, config)
- Le contrat d'interface : backend.schemas (Pydantic v2)
"""

from contextlib import asynccontextmanager
from unittest import result
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from iatos_core import __version__
from iatos_core.logger import logger
from iatos_core.ml.scoring import CreditScoringPredictor
from iatos_core.ml.sentiment import SentimentAnalyzer
from iatos_core.ml.classifier import TicketClassifier
from iatos_core.agent.graph import run_agent_message

from backend.schemas import (
    ChatRequest,
    ChatResponse,
    CreditPredictRequest,
    CreditPredictResponse,
    HealthResponse,
    SentimentPredictRequest,
    SentimentPredictResponse,
    TicketRouteRequest,
    TicketRouteResponse,
    CategoryScore,
)

# Services partages (Singletons en memoire)
scoring_predictor: CreditScoringPredictor = None
sentiment_analyzer: SentimentAnalyzer = None
category_classifier: TicketClassifier = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cycle de vie de l'application FastAPI.
    
    TODO (Apprenants) :
    1. Instancier le CreditScoringPredictor() et l'assigner a la variable globale scoring_predictor.
    2. Instancier le SentimentAnalyzer() et l'assigner a la variable globale sentiment_analyzer.
    3. Logger le succes de l'initialisation avec loguru.
    """
    global scoring_predictor, sentiment_analyzer, category_classifier
    logger.info("Demarrage des services FastAPI IA-TOS...")
    
    scoring_predictor = CreditScoringPredictor()
    sentiment_analyzer = SentimentAnalyzer()
    category_classifier = TicketClassifier()
    logger.info("Services FastAPI IA-TOS demarrés avec succes.")
    
    yield
    logger.info("Arret des services FastAPI IA-TOS.")


# Instanciation de l'application FastAPI
app = FastAPI(
    title="Plateforme IA-TOS - API Multi-Services",
    description="API exposant l'agent conversationnel LangGraph, le scoring de credit et l'analyse de sentiment.",
    version=__version__,
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Supervision"])
def health_check():
    """Endpoint de surveillance (Healthcheck) pour Uptime Kuma ou Docker.
    
    TODO (Apprenants) :
    Retourner une instance de HealthResponse avec :
    - status="ok"
    - version=__version__
    - service="iatos-api"
    """
    # TODO: Remplacer par votre implementation
    return HealthResponse(
        status="ok", 
        version=__version__, 
        service="iatos-api"
    )


@app.post("/chat", response_model=ChatResponse, tags=["Agent Conversationnel"])
def chat_endpoint(payload: ChatRequest):
    """Endpoint conversationnel interrogeant l'agent LangGraph outille.
    
    TODO (Apprenants) :
    1. Convertir l'historique Pydantic (payload.history) en liste de dictionnaires [{'role': ..., 'content': ...}].
    2. Appeler run_agent_message(user_message=payload.message, history=history_dicts).
    3. Retourner une instance de ChatResponse avec :
       - success (bool)
       - response (str)
       - tool_called (bool)
       - tool_results (list[str])
    4. Gerer les exceptions potentielles avec un logger.error et un HTTPException(500).
    """
    # TODO: Remplacer par votre implementation

    history_dicts = [
    {"role": message.role, "content": message.content}
    for message in payload.history
]   
    try:
        result = run_agent_message(
            user_message=payload.message,
            history=history_dicts,
        )
    
        return ChatResponse(
            success=result["success"],
            response=result["response"],
            tool_called=result["tool_called"],
            tool_results=result["tool_results"],
        )
    except Exception as exc:
        logger.error("Erreur inattendue dans l'endpoint /chat")
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue.",
        ) from exc


@app.post("/predict/credit", response_model=CreditPredictResponse, tags=["Scoring Tabulaire"])
def predict_credit(payload: CreditPredictRequest):
    """Endpoint de prediction du score de credit (baseline Scikit-Learn M0).
    
    TODO (Apprenants) :
    1. Recuperer l'instance globale de scoring_predictor (ou l'instancier si None).
    2. Appeler scoring_predictor.predict(...) avec montant_demande, duree_mois et revenu_mensuel.
    3. Retourner une instance de CreditPredictResponse avec les resultats.
    4. Gerer les exceptions potentielles avec un HTTPException(500).
    """
    # TODO: Remplacer par votre implementation
    try:
        global scoring_predictor
        if scoring_predictor is None:
            scoring_predictor = CreditScoringPredictor()
        
        prediction_result = scoring_predictor.predict(
            montant_demande=payload.montant_demande,
            duree_mois=payload.duree_mois,
            revenu_mensuel=payload.revenu_mensuel
        )
        
        return CreditPredictResponse(
            score=prediction_result["score"],
            decision=prediction_result["decision"],
            motif=prediction_result["motif"],
            features_utilisees=prediction_result["features_utilisees"],
            type_modele=prediction_result["type_modele"]
        )
    except Exception as exc:
            logger.error("Erreur inattendue dans l'endpoint /predict/credit")
            raise HTTPException(
                status_code=500,
                detail="Une erreur interne est survenue.",
            ) from exc


@app.post("/predict/sentiment", response_model=SentimentPredictResponse, tags=["Traitement NLP"])
def predict_sentiment(payload: SentimentPredictRequest):
    """Endpoint d'analyse de polarite de sentiment (baseline NLTK VADER M0).
    
    TODO (Apprenants) :
    1. Recuperer l'instance globale de sentiment_analyzer (ou l'instancier si None).
    2. Appeler sentiment_analyzer.analyze(payload.texte).
    3. Retourner une instance de SentimentPredictResponse avec les resultats.
    4. Gerer les exceptions potentielles avec un HTTPException(500).
    """
    # TODO: Remplacer par votre implementation
    try:
        global sentiment_analyzer
        if sentiment_analyzer is None:
            sentiment_analyzer = SentimentAnalyzer()
        
        analysis_result = sentiment_analyzer.analyze(payload.texte)
        
        return SentimentPredictResponse(
            texte=payload.texte,
            compound=analysis_result["compound"],
            label=analysis_result["label"],
            scores=analysis_result["scores"],
            type_modele=analysis_result["type_modele"]
        )
    except Exception as exc:
        logger.error("Erreur inattendue dans l'endpoint /predict/sentiment")
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue.",
        ) from exc

@app.post("/classify-ticket", response_model=TicketRouteResponse, tags=["Traitement Zero-Shot"])
def classify_ticket(payload: TicketRouteRequest):
    """Endpoint de routage de tickets vers des catégories.
    """
    try:
        global category_classifier
        if category_classifier is None:
            category_classifier = TicketClassifier()
        
        result = category_classifier.classify(payload.ticket_text, payload.categories)
        
        return TicketRouteResponse(**result)
    except Exception as exc:
        logger.error("Erreur inattendue dans l'endpoint /categorize")
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue.",
        ) from exc