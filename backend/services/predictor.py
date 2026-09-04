import os
import logging
import joblib
import numpy as np
from backend.core import config
from backend.models.pydantic_models import SymptomRequest

logger = logging.getLogger("vishalya.predictor")

# Model path resolution relative to project root
MODEL_PATH = config.PROJECT_ROOT / "ml_engine" / "vishalya_rf_model.joblib"

FEATURE_ORDER = [
    "fever",
    "cough",
    "shortness_of_breath",
    "sore_throat",
    "diarrhea",
    "vomiting",
    "headache",
    "fatigue",
    "skin_rash",
    "chills",
    "aqi_level"
]


class PredictorServiceError(Exception):
    """Raised when model loading or inference fails."""
    pass


class RiskPredictorService:
    """
    Singleton ML Inference Service loading the trained Random Forest Joblib model once.
    """
    def __init__(self, model_path: str = str(MODEL_PATH)):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise PredictorServiceError(
                f"ML model file 'ml_engine/vishalya_rf_model.joblib' could not be found at: {self.model_path}"
            )
        try:
            logger.info("Loading Joblib Random Forest model into memory...")
            return joblib.load(self.model_path)
        except Exception as err:
            raise PredictorServiceError(f"Failed to load Joblib model: {err}")

    def predict(self, symptoms: SymptomRequest, aqi_level: float) -> int:
        """
        Constructs NumPy 2D array matching strict 11-feature order and runs inference.
        Returns: 0 (LOW risk) or 1 (HIGH risk).
        """
        if self.model is None:
            raise PredictorServiceError("Joblib ML model is not loaded.")

        # Construct feature array in exact order
        feature_vector = [
            symptoms.fever,
            symptoms.cough,
            symptoms.shortness_of_breath,
            symptoms.sore_throat,
            symptoms.diarrhea,
            symptoms.vomiting,
            symptoms.headache,
            symptoms.fatigue,
            symptoms.skin_rash,
            symptoms.chills,
            aqi_level
        ]

        # Shape: (1, 11)
        input_matrix = np.array([feature_vector], dtype=float)

        try:
            raw_result = self.model.predict(input_matrix)
            prediction = int(raw_result[0])
            if prediction not in (0, 1):
                raise ValueError(f"Invalid model prediction output: {prediction}")
            return prediction
        except Exception as err:
            raise PredictorServiceError(f"ML inference error: {err}")


# Singleton instance
_predictor_instance = None
_predictor_error = None

try:
    _predictor_instance = RiskPredictorService()
except Exception as _err:
    _predictor_error = _err


def get_predictor() -> RiskPredictorService:
    if _predictor_instance is None or _predictor_instance.model is None:
        if _predictor_error:
            raise _predictor_error
        raise PredictorServiceError("ML model file 'ml_engine/vishalya_rf_model.joblib' is not available.")
    return _predictor_instance
