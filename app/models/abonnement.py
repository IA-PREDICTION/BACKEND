import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Date, Enum, ForeignKey
from sqlalchemy import text
from app.db.base_class import Base

class StatutAbonnement(str, enum.Enum):
    actif = "actif"
    expire = "expire"
    annule = "annule"
    suspendu = "suspendu"

class Abonnement(Base):
    __tablename__ = "abonnements"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans_abonnement.id", ondelete="RESTRICT"), nullable=False)
    date_debut = Column(TIMESTAMP, nullable=False)
    date_fin = Column(TIMESTAMP, nullable=False)
    statut = Column(Enum(StatutAbonnement, name="statut_abonnement_enum", native_enum=True), nullable=False, server_default=text("'actif'"))
    periode_essai = Column(Boolean, nullable=False, server_default=text("false"))
    auto_renouvellement = Column(Boolean, nullable=False, server_default=text("true"))
    nb_pronostics_jour_utilises = Column(Integer, nullable=False, server_default=text("0"))
    date_reset_quotidien = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
