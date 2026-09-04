"""
Backward-compatibility bridge forwarding predictor imports to backend.services.predictor.
"""
from backend.services.predictor import (
    RiskPredictorService as RiskPredictor,
    PredictorServiceError as ModelPredictionError,
    PredictorServiceError as ModelNotFoundError,
    get_predictor,
    FEATURE_ORDER,
)

__all__ = [
    "RiskPredictor",
    "ModelPredictionError",
    "ModelNotFoundError",
    "get_predictor",
    "FEATURE_ORDER",
]
