from pydantic import BaseModel
from datetime import date, datetime

class MonitoringBase(BaseModel):
    modele_id: int
    date_evaluation: date
    nb_predictions: int | None = None
    accuracy_reelle: float | None = None
    drift_score: float | None = None
    alertes: dict | None = None
    recommendations: str | None = None

class MonitoringCreate(MonitoringBase): pass
class MonitoringUpdate(BaseModel):
    nb_predictions: int | None = None
    accuracy_reelle: float | None = None
    drift_score: float | None = None
    alertes: dict | None = None
    recommendations: str | None = None

class MonitoringOut(MonitoringBase):
    id: int
    created_at: datetime | None = None
    class Config:
        from_attributes = True
