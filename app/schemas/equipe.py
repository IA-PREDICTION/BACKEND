from pydantic import BaseModel

class EquipeBase(BaseModel):
    nom: str
    nom_court: str | None = None
    sport_id: int
    pays: str | None = None
    logo_url: str | None = None
    stade: str | None = None
    api_id: str | None = None

class EquipeCreate(EquipeBase): pass
class EquipeUpdate(BaseModel):
    nom: str | None = None
    nom_court: str | None = None
    sport_id: int | None = None
    pays: str | None = None
    logo_url: str | None = None
    stade: str | None = None
    api_id: str | None = None

class EquipeOut(EquipeBase):
    id: int
    class Config:
        from_attributes = True
