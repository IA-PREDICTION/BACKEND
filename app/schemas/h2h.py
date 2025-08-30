from pydantic import BaseModel
from datetime import datetime

class H2HBase(BaseModel):
    equipe1_id: int
    equipe2_id: int
    match_id: int
    date_match: datetime
    score_equipe1: int | None = None
    score_equipe2: int | None = None
    lieu: str | None = None  # 'domicile_eq1' | 'domicile_eq2' | 'neutre'
    championnat_id: int | None = None

class H2HCreate(H2HBase): pass

class H2HUpdate(BaseModel):
    score_equipe1: int | None = None
    score_equipe2: int | None = None
    lieu: str | None = None
    championnat_id: int | None = None

class H2HOut(H2HBase):
    id: int
    class Config:
        from_attributes = True
