from pydantic import BaseModel
from datetime import date

class BlessureBase(BaseModel):
    joueur_id: int
    equipe_id: int
    type: str    # 'blessure' | 'suspension' | 'autre'
    gravite: str | None = None  # 'legere' | 'moyenne' | 'grave'
    date_debut: date
    date_fin_prevue: date | None = None
    match_id: int | None = None
    description: str | None = None
    source: str | None = None

class BlessureCreate(BlessureBase): pass

class BlessureUpdate(BaseModel):
    type: str | None = None
    gravite: str | None = None
    date_fin_prevue: date | None = None
    match_id: int | None = None
    description: str | None = None
    source: str | None = None

class BlessureOut(BlessureBase):
    id: int
    class Config:
        from_attributes = True
