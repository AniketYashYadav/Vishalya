from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


class SymptomRequest(BaseModel):
    """
    Syndromic indicator values (0 = absent, 1 = present).
    """
    fever: int = Field(0, description="0 = absent, 1 = present")
    cough: int = Field(0, description="0 = absent, 1 = present")
    shortness_of_breath: int = Field(0, description="0 = absent, 1 = present")
    sore_throat: int = Field(0, description="0 = absent, 1 = present")
    diarrhea: int = Field(0, description="0 = absent, 1 = present")
    vomiting: int = Field(0, description="0 = absent, 1 = present")
    headache: int = Field(0, description="0 = absent, 1 = present")
    fatigue: int = Field(0, description="0 = absent, 1 = present")
    skin_rash: int = Field(0, description="0 = absent, 1 = present")
    chills: int = Field(0, description="0 = absent, 1 = present")

    @field_validator(
        "fever", "cough", "shortness_of_breath", "sore_throat",
        "diarrhea", "vomiting", "headache", "fatigue",
        "skin_rash", "chills",
        mode="before"
    )
    @classmethod
    def validate_binary(cls, v: int) -> int:
        if isinstance(v, bool):
            return 1 if v else 0
        try:
            val = int(v)
        except (TypeError, ValueError):
            raise ValueError("Symptom value must be an integer (0 or 1).")
        if val not in (0, 1):
            raise ValueError("Symptom value must be strictly 0 (absent) or 1 (present).")
        return val


class PredictionRequest(BaseModel):
    """
    Payload sent by frontend / tablet background sync engine.
    If aqi_level is omitted or null, live AQI is dynamically pulled.
    """
    patient_id: str = Field(..., min_length=1, description="Patient identifier")
    village_pin: str = Field(..., min_length=1, description="Village PIN / postal code")
    latitude: Optional[float] = Field(None, description="GPS Latitude coordinate")
    longitude: Optional[float] = Field(None, description="GPS Longitude coordinate")
    symptoms: SymptomRequest
    aqi_level: Optional[float] = Field(None, description="Numeric AQI (auto-fetched if omitted)")
    timestamp: Optional[str] = Field(None, description="ISO-8601 timestamp string")

    @field_validator("patient_id", "village_pin")
    @classmethod
    def validate_non_empty(cls, v: str, info) -> str:
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} cannot be empty or whitespace.")
        return str(v).strip()


class PredictionResponse(BaseModel):
    """
    JSON response containing outbreak risk prediction and AQI tracking data.
    """
    patient_id: str
    risk_label: Literal["HIGH", "LOW"]
    risk_score: Literal[0, 1]
    aqi_used: float
    aqi_source: str = Field("payload_provided", description="Source of AQI value")
    timestamp: Optional[str] = None
