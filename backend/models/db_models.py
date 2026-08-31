from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.core.database import Base


class PatientSyncRecord(Base):
    """
    Database table storing patient sync payloads and eco-syndromic prediction results.
    """
    __tablename__ = "patient_sync_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String(64), index=True, nullable=False)
    village_pin = Column(String(16), index=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    symptoms_json = Column(Text, nullable=False)
    aqi_level = Column(Float, nullable=False)
    risk_label = Column(String(16), nullable=False)
    risk_score = Column(Integer, nullable=False)
    synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    timestamp = Column(String(64), nullable=True)

    def __repr__(self):
        return f"<PatientSyncRecord(patient_id='{self.patient_id}', risk='{self.risk_label}')>"
