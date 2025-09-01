import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class PlanAbonnement(Base):
    __tablename__ = "plans_abonnement"

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    prix = Column(Numeric(10,2), nullable=False)
    duree_jours = Column(Integer, nullable=False)
    nb_pronostics_jour = Column(Integer, nullable=True)
    sports_autorises = Column(JSONB, nullable=True)
    acces_stats_avancees = Column(Boolean, nullable=False, server_default=text("false"))
    acces_predictions_ia = Column(Boolean, nullable=False, server_default=text("true"))
    acces_historique_complet = Column(Boolean, nullable=False, server_default=text("false"))
    acces_api = Column(Boolean, nullable=False, server_default=text("false"))
    priority_support = Column(Boolean, nullable=False, server_default=text("false"))
    periode_essai_jours = Column(Integer, nullable=False, server_default=text("0"))
    actif = Column(Boolean, nullable=False, server_default=text("true"))
    ordre_affichage = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
