from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
import enum
from app.db.base_class import Base

try:
    from app.core.config import settings
    DB_SCHEMA = getattr(settings, "DB_SCHEMA", "public")
except Exception:
    DB_SCHEMA = "public"


class StatutIngestion(str, enum.Enum):
    succes = "succes"
    partiel = "partiel"
    echec = "echec"


class LogIngestion(Base):
    __tablename__ = "logs_ingestion"
    __table_args__ = (
        ForeignKeyConstraint(["source_id"], [f"{DB_SCHEMA}.sources_donnees.id"], ondelete="CASCADE"),
        {"schema": DB_SCHEMA},
    )

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, nullable=False)
    type_donnees = Column(String(50))  # 'matchs', 'stats', 'cotes', etc.
    nb_enregistrements = Column(Integer)
    nb_nouveaux = Column(Integer)
    nb_modifies = Column(Integer)
    nb_erreurs = Column(Integer)
    duree_secondes = Column(Integer)
    statut = Column(Enum(StatutIngestion, name="statut_ingestion_enum", native_enum=True))
    erreurs = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
