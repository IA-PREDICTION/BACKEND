from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PronosticBase(BaseModel):
    match_id: int
    prediction_id: Optional[int] = None
    choix_utilisateur: Optional[str] = None   # "1","X","2"
    score_predit_dom: Optional[int] = None
    score_predit_ext: Optional[int] = None
    mise_virtuelle: Optional[float] = 0
    cote: Optional[float] = None
    partage_public: bool = False
    note_confiance: Optional[int] = None

class PronosticCreate(PronosticBase):
    pass

class PronosticUpdate(BaseModel):
    choix_utilisateur: Optional[str] = None
    score_predit_dom: Optional[int] = None
    score_predit_ext: Optional[int] = None
    mise_virtuelle: Optional[float] = None
    cote: Optional[float] = None
    partage_public: Optional[bool] = None
    note_confiance: Optional[int] = None

class PronosticOut(PronosticBase):
    id: int
    user_id: int
    date_pronostic: datetime
    resultat: str
    gains_virtuels: float

    class Config:
        from_attributes = True
