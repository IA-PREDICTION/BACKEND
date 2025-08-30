from pydantic import BaseModel
from datetime import date

class JoueurBase(BaseModel):
    nom: str
    prenom: str | None = None
    equipe_id: int | None = None
    position: str | None = None
    numero: int | None = None
    date_naissance: date | None = None
    nationalite: str | None = None
    valeur_marchande: float | None = None
    api_id: str | None = None
    actif: bool = True

class JoueurCreate(JoueurBase): pass

class JoueurUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    equipe_id: int | None = None
    position: str | None = None
    numero: int | None = None
    date_naissance: date | None = None
    nationalite: str | None = None
    valeur_marchande: float | None = None
    api_id: str | None = None
    actif: bool | None = None

class JoueurOut(JoueurBase):
    id: int
    class Config:
        from_attributes = True
