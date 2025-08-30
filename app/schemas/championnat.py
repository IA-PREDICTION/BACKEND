from pydantic import BaseModel

class ChampionnatBase(BaseModel):
    sport_id: int
    nom: str
    pays: str | None = None
    niveau: int | None = None
    saison_actuelle: str | None = None
    logo_url: str | None = None
    api_id: str | None = None
    actif: bool = True

class ChampionnatCreate(ChampionnatBase): pass
class ChampionnatUpdate(BaseModel):
    sport_id: int | None = None
    nom: str | None = None
    pays: str | None = None
    niveau: int | None = None
    saison_actuelle: str | None = None
    logo_url: str | None = None
    api_id: str | None = None
    actif: bool | None = None

class ChampionnatOut(ChampionnatBase):
    id: int
    class Config:
        from_attributes = True
