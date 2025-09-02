from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict, Literal
from datetime import datetime

# Pydantic v2 : from_attributes=True (ex-orm_mode)
class SourceDonneeBase(BaseModel):
    nom: str
    type: Literal["api", "scraping", "manual"]
    url_base: Optional[str] = None
    api_key_encrypted: Optional[str] = None
    frequence_maj_minutes: Optional[int] = None
    statut: Optional[Literal["actif", "pause", "erreur"]] = "actif"
    configuration: Optional[Dict[str, Any]] = None
    rate_limit_par_heure: Optional[int] = None

class SourceDonneeCreate(SourceDonneeBase):
    pass

class SourceDonneeUpdate(BaseModel):
    nom: Optional[str] = None
    type: Optional[Literal["api", "scraping", "manual"]] = None
    url_base: Optional[str] = None
    api_key_encrypted: Optional[str] = None
    frequence_maj_minutes: Optional[int] = None
    statut: Optional[Literal["actif", "pause", "erreur"]] = None
    configuration: Optional[Dict[str, Any]] = None
    rate_limit_par_heure: Optional[int] = None
    prochaine_synchro: Optional[datetime] = None

class SourceDonneeOut(SourceDonneeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    derniere_synchro: Optional[datetime] = None
    prochaine_synchro: Optional[datetime] = None
    created_at: Optional[datetime] = None


class LogIngestionBase(BaseModel):
    source_id: int
    type_donnees: Optional[str] = None
    nb_enregistrements: Optional[int] = 0
    nb_nouveaux: Optional[int] = 0
    nb_modifies: Optional[int] = 0
    nb_erreurs: Optional[int] = 0
    duree_secondes: Optional[int] = 0
    statut: Optional[Literal["succes", "partiel", "echec"]] = "succes"
    erreurs: Optional[Dict[str, Any]] = None

class LogIngestionCreate(LogIngestionBase):
    pass

class LogIngestionOut(LogIngestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: Optional[datetime] = None
