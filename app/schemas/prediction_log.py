from pydantic import BaseModel
from datetime import datetime

class PredLogBase(BaseModel):
    prediction_id: int
    match_id: int
    modele_id: int
    input_features: dict | None = None
    output_raw: dict | None = None
    temps_inference_ms: int | None = None
    version_api: str | None = None
    erreur: str | None = None

class PredLogCreate(PredLogBase): pass

class PredLogOut(PredLogBase):
    id: int
    created_at: datetime | None = None
    class Config:
        from_attributes = True
