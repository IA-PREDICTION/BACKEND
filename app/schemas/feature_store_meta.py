from pydantic import BaseModel

class FeatureMetaBase(BaseModel):
    nom_feature: str
    description: str | None = None
    type_donnee: str | None = None
    source: str | None = None
    formule_calcul: str | None = None
    importance_moyenne: float | None = None
    statut: str | None = "actif"
    version: str | None = None

class FeatureMetaCreate(FeatureMetaBase): pass
class FeatureMetaUpdate(BaseModel):
    description: str | None = None
    type_donnee: str | None = None
    source: str | None = None
    formule_calcul: str | None = None
    importance_moyenne: float | None = None
    statut: str | None = None
    version: str | None = None

class FeatureMetaOut(FeatureMetaBase):
    id: int
    class Config:
        from_attributes = True
