"""Module de routage de tickets vers des catégories."""

from typing import Dict, Any
from iatos_core.logger import logger
from transformers import pipeline




class TicketClassifier:
    """Catégoriseur de tickets utilisant un modèle de classification zero-shot basé sur DeBERTa-v3."""

    def __init__(self):
        self.classifier = pipeline('zero-shot-classification', model='MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli')
        logger.info("Classifier initialise.")

    def classify(self, ticket_texte: str, categories: list[str]) -> Dict[str, Any]:
        """Catégorise un texte donné.
        
        Args:
            ticket_texte: Texte du ticket a catégoriser.
            categories: Liste des catégories cibles pour la classification.
            
        Returns:
            Dictionnaire avec le score compound, le label et les scores elementaires.
        """
    
        ticket_texte_clean = ticket_texte.strip()
        if not ticket_texte_clean:
            logger.error("Texte vide transmis pour la classification.")
            return {
                "top_category": "Non classifié",
                "confidence": 0.0,
                "distribution": [],
            }
        result = self.classifier(
            ticket_texte_clean, 
            candidate_labels=categories
            )
        distribution = [
        {"category": category, "score": float(score)}
        for category, score in zip(result["labels"], result["scores"])
    ]


        logger.info("Classification pour '{t}...' : category={c}", t=ticket_texte_clean[:30], c=categories)

        return {
                "top_category": result["labels"][0],
                "confidence": float(result["scores"][0]),
                "distribution": distribution
            }
