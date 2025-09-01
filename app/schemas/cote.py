from pydantic import BaseModel
from datetime import datetime

class CoteBase(BaseModel):
    match_id: int
    bookmaker: str
    cote_dom: float
    cote_nul: float | None = None
    cote_ext: float
    cote_over_2_5: float | None = None
    cote_under_2_5: float | None = None
    cote_btts_oui: float | None = None
    cote_btts_non: float | None = None
    date_maj: datetime

class CoteCreate(CoteBase): pass

class CoteUpdate(BaseModel):
    cote_dom: float | None = None
    cote_nul: float | None = None
    cote_ext: float | None = None
    cote_over_2_5: float | None = None
    cote_under_2_5: float | None = None
    cote_btts_oui: float | None = None
    cote_btts_non: float | None = None

class CoteOut(CoteBase):
    id: int
    class Config:
        from_attributes = True
