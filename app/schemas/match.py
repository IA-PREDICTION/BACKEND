from pydantic import BaseModel
from datetime import datetime

class MatchBase(BaseModel):
    sport_id: int
    championnat_id: int
    equipe_dom_id: int
    equipe_ext_id: int
    date_match: datetime
    journee: int | None = None
    statut: str | None = None  # 'a_venir' | 'en_cours' | ...
    minute_actuelle: int | None = None
    api_id: str | None = None
    importance_match: int | None = 1
    diffusion_tv: str | None = None
    arbitre: str | None = None

class MatchCreate(MatchBase): pass
class MatchUpdate(BaseModel):
    sport_id: int | None = None
    championnat_id: int | None = None
    equipe_dom_id: int | None = None
    equipe_ext_id: int | None = None
    date_match: datetime | None = None
    journee: int | None = None
    statut: str | None = None
    minute_actuelle: int | None = None
    api_id: str | None = None
    importance_match: int | None = None
    diffusion_tv: str | None = None
    arbitre: str | None = None

class MatchOut(MatchBase):
    id: int
    score_dom: int | None = None
    score_ext: int | None = None
    score_mi_temps_dom: int | None = None
    score_mi_temps_ext: int | None = None

    class Config:
        from_attributes = True
