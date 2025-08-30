from pydantic import BaseModel

class SportBase(BaseModel):
    nom: str
    code: str
    icone: str | None = None
    actif: bool = True

class SportCreate(SportBase): pass
class SportUpdate(BaseModel):
    nom: str | None = None
    code: str | None = None
    icone: str | None = None
    actif: bool | None = None

class SportOut(SportBase):
    id: int
    class Config:
        from_attributes = True
