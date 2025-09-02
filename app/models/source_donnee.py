import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

# ⚠️ Schéma : on prend depuis settings si présent, sinon "public"
try:
    from app.core.config import settings
    DB_SCHEMA = getattr(settings, "DB_SCHEMA", "public")
except Exception:
    DB_SCHEMA = "public"


class TypeSource(str, enum.Enum):
    api = "api"
    scraping = "scraping"
    manual = "manual"


class StatutSource(str, enum.Enum):
    actif = "actif"
    pause = "pause"
    erreur = "erreur"


class SourceDonnee(Base):
    __tablename__ = "sources_donnees"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    type = Column(Enum(TypeSource, name="type_source_enum", native_enum=True), nullable=False)
    url_base = Column(String(255))
    api_key_encrypted = Column(String(255))
    frequence_maj_minutes = Column(Integer)
    derniere_synchro = Column(TIMESTAMP)
    prochaine_synchro = Column(TIMESTAMP)
    statut = Column(Enum(StatutSource, name="statut_source_enum", native_enum=True), nullable=False, server_default=text("'actif'"))
    configuration = Column(JSONB)
    rate_limit_par_heure = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
