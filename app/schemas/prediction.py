from pydantic import BaseModel
from datetime import datetime

class PredictionBase(BaseModel):
    match_id: int
    modele_id: int
    type_prediction: str | None = None
    proba_victoire_dom: float | None = None
    proba_nul: float | None = None
    proba_victoire_ext: float | None = None
    prediction_finale: str | None = None  # '1' | 'X' | '2'
    confidence: float | None = None
    score_predit_dom: int | None = None
    score_predit_ext: int | None = None
    total_buts_predit: float | None = None
    proba_over_2_5: float | None = None
    proba_under_2_5: float | None = None
    proba_btts_oui: float | None = None
    proba_btts_non: float | None = None
    features_importance: dict | None = None
    shap_values: dict | None = None
    batch_id: str | None = None
    temps_calcul_ms: int | None = None

class PredictionCreate(PredictionBase): pass

class PredictionUpdate(BaseModel):
    prediction_finale: str | None = None
    confidence: float | None = None
    features_importance: dict | None = None
    shap_values: dict | None = None

class PredictionOut(PredictionBase):
    id: int
    date_prediction: datetime | None = None
    class Config:
        from_attributes = True
