import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.db_models import PatientSyncRecord
from backend.models.pydantic_models import PredictionRequest, PredictionResponse
from backend.services.predictor import get_predictor, PredictorServiceError
from backend.services.weather_api import get_live_aqi

logger = logging.getLogger("vishalya.router.sync")

router = APIRouter(prefix="/api", tags=["Patient Sync & Outbreak Risk"])


@router.post(
    "/sync-patients",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Synchronize Patient Data & Predict Risk",
    description="Receives background ASHA sync payload, pulls live AQI if needed, runs ML inference, and logs to database pool."
)
@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Outbreak Risk",
    description="Predicts eco-syndromic outbreak risk for a patient record."
)
async def sync_and_predict_patient(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    # 1. Determine AQI level (use payload value or pull live AQI from OpenWeather API)
    if request.aqi_level is not None:
        aqi_used = float(request.aqi_level)
        aqi_source = "payload_provided"
    else:
        aqi_used, aqi_source = await get_live_aqi(
            latitude=request.latitude,
            longitude=request.longitude,
            village_pin=request.village_pin
        )

    # 2. Run ML model inference
    try:
        predictor = get_predictor()
        prediction_code = predictor.predict(
            symptoms=request.symptoms,
            aqi_level=aqi_used
        )
    except PredictorServiceError as err:
        logger.error(f"Inference failed for patient {request.patient_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    except Exception as err:
        logger.exception(f"Unexpected prediction failure for patient {request.patient_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during risk evaluation."
        )

    risk_label = "HIGH" if prediction_code == 1 else "LOW"
    risk_score = 1 if prediction_code == 1 else 0

    # 3. Log patient sync record into central database connection pool
    try:
        db_record = PatientSyncRecord(
            patient_id=request.patient_id,
            village_pin=request.village_pin,
            latitude=request.latitude,
            longitude=request.longitude,
            symptoms_json=json.dumps(request.symptoms.model_dump()),
            aqi_level=aqi_used,
            risk_label=risk_label,
            risk_score=risk_score,
            timestamp=request.timestamp
        )
        db.add(db_record)
        db.commit()
    except Exception as err:
        db.rollback()
        logger.error(f"Database logging failed for patient {request.patient_id}: {err}")
        # Proceed with returning prediction response even if DB logging encounters a temporary glitch

    return PredictionResponse(
        patient_id=request.patient_id,
        risk_label=risk_label,
        risk_score=risk_score,
        aqi_used=aqi_used,
        aqi_source=aqi_source,
        timestamp=request.timestamp
    )
