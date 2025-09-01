from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class FeatureStoreMeta(Base):
    __tablename__ = "feature_store_metadata"

    id = Column(Integer, primary_key=True)
    nom_feature = Column(String(100), nullable=False, unique=True)
    description = Column(String)
    type_donnee = Column(String(50))
    source = Column(String(100))
    formule_calcul = Column(String)
    importance_moyenne = Column(Numeric(5,2))
    statut = Column(String(20), server_default=text("'actif'"))
    version = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
