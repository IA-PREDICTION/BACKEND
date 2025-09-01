from pydantic import BaseModel
from datetime import datetime

class MLModelBase(BaseModel):
    nom: str
    version: str
    sport_id: int
    type_prediction: str | None = None
    algorithme: str | None = None
    accuracy: float | None = None
    precision_score: float | None = None
    recall_score: float | None = None
    f1_score: float | None = None
    date_entrainement: datetime
    date_deploiement: datetime | None = None
    statut: str | None = None
    hyperparametres: dict | None = None
    features_utilisees: dict | None = None
    chemin_modele: str | None = None
    taille_mb: float | None = None
    temps_entrainement_minutes: int | None = None
    dataset_version: str | None = None
    created_by: int | None = None

class MLModelCreate(MLModelBase): pass

class MLModelUpdate(BaseModel):
    nom: str | None = None
    version: str | None = None
    type_prediction: str | None = None
    algorithme: str | None = None
    accuracy: float | None = None
    precision_score: float | None = None
    recall_score: float | None = None
    f1_score: float | None = None
    date_deploiement: datetime | None = None
    statut: str | None = None
    hyperparametres: dict | None = None
    features_utilisees: dict | None = None
    chemin_modele: str | None = None
    taille_mb: float | None = None
    temps_entrainement_minutes: int | None = None
    dataset_version: str | None = None

class MLModelOut(MLModelBase):
    id: int
    created_at: datetime | None = None
    class Config:
        from_attributes = True
