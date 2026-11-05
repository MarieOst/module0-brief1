"""Schemas Pydantic pour l'API FastAPI."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


# Schemas pour le Chatbot LangGraph
class ChatMessage(BaseModel):
    role: str = Field(..., description="Role de l'emetteur : 'user' ou 'assistant'")
    content: str = Field(..., description="Contenu texte du message")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message saisi par l'utilisateur")
    history: List[ChatMessage] = Field(default_factory=list, description="Historique de la conversation")


class ChatResponse(BaseModel):
    success: bool
    response: str
    tool_called: bool
    tool_results: List[str] = Field(default_factory=list)


# Schemas pour la Prediction de Credit
class CreditPredictRequest(BaseModel):
    montant_demande: float = Field(..., gt=0, le=500000, description="Montant souhaite en euros")
    duree_mois: int = Field(..., ge=6, le=360, description="Duree du pret en mois")
    revenu_mensuel: float = Field(..., gt=0, le=100000, description="Revenu mensuel net en euros")


class CreditPredictResponse(BaseModel):
    score: float
    decision: str
    motif: str
    features_utilisees: Dict[str, float]
    type_modele: str


# Schemas pour l'Analyse de Sentiment
class SentimentPredictRequest(BaseModel):
    texte: str = Field(..., min_length=1, description="Texte de l'avis ou du message a analyser")


class SentimentPredictResponse(BaseModel):
    texte: str
    compound: float
    label: str
    scores: Dict[str, float]
    type_modele: str


# Schema de statut de service
class HealthResponse(BaseModel):
    status: str
    version: str
    service: str

# Schema pour la classification zero-shot
class TicketRouteRequest(BaseModel):
    ticket_text: str = Field(..., min_length=10, description="Texte descriptif de l'incident ou de la demande")
    categories: list[str] = Field(..., min_length=2, description="Liste dynamique des départements ou thèmes cibles")

class CategoryScore(BaseModel):
    category: str
    score: float

class TicketRouteResponse(BaseModel):
    top_category: str
    confidence: float
    distribution: list[CategoryScore]