from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base


# Enum pour statut abonnements
class StatutAbonnement(str, enum.Enum):
    actif = "actif"
    expire = "expire"
    annule = "annule"
    suspendu = "suspendu"


class PlanAbonnement(Base):
    __tablename__ = "plans_abonnement"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    prix = Column(Numeric(10, 2), nullable=False)
    duree_jours = Column(Integer, nullable=False)
    nb_pronostics_jour = Column(Integer, nullable=True)  # NULL = illimité
    acces_stats_avancees = Column(Boolean, default=False)
    acces_predictions_ia = Column(Boolean, default=True)
    acces_historique_complet = Column(Boolean, default=False)
    acces_api = Column(Boolean, default=False)
    priority_support = Column(Boolean, default=False)
    periode_essai_jours = Column(Integer, default=0)
    actif = Column(Boolean, default=True)
    ordre_affichage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Abonnement(Base):
    __tablename__ = "abonnements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans_abonnement.id", ondelete="RESTRICT"), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    statut = Column(Enum(StatutAbonnement), default=StatutAbonnement.actif, nullable=False)
    periode_essai = Column(Boolean, default=False)
    auto_renouvellement = Column(Boolean, default=True)
    nb_pronostics_jour_utilises = Column(Integer, default=0)
    date_reset_quotidien = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    plan = relationship("PlanAbonnement", backref="abonnements")
    user = relationship("Utilisateur", back_populates="abonnements")

