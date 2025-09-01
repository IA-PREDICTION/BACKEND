from pydantic import BaseModel
from typing import Any, Dict, Literal

class PredictRequest(BaseModel):
    match_id: int
    modele_id: int
    type_prediction: Literal["match_result", "score_exact", "over_under", "both_teams_score"] = "match_result"
    # Optionnel: override des features si tu veux forcer des valeurs au lieu de charger la DB
    override_features: Dict[str, Any] | None = None

class PredictResponse(BaseModel):
    prediction_id: int
    match_id: int
    modele_id: int
    type_prediction: str
    prediction_finale: str | None = None
    confidence: float | None = None
    proba_victoire_dom: float | None = None
    proba_nul: float | None = None
    proba_victoire_ext: float | None = None
