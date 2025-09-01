import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.db.base_class import Base

class TypePrediction(str, enum.Enum):
    match_result = "match_result"
    score_exact = "score_exact"
    over_under = "over_under"
    both_teams_score = "both_teams_score"

class StatutModele(str, enum.Enum):
    entrainement = "entrainement"
    validation = "validation"
    production = "production"
    archive = "archive"

class ModeleIA(Base):
    __tablename__ = "modeles_ia"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    type_prediction = Column(Enum(TypePrediction, name="type_prediction_enum", native_enum=True), nullable=True)
    algorithme = Column(String(50))
    accuracy = Column(Numeric(5,2))
    precision_score = Column(Numeric(5,2))
    recall_score = Column(Numeric(5,2))
    f1_score = Column(Numeric(5,2))
    date_entrainement = Column(TIMESTAMP, nullable=False)
    date_deploiement = Column(TIMESTAMP)
    statut = Column(Enum(StatutModele, name="statut_modele_enum", native_enum=True), nullable=False, server_default=text("'entrainement'"))
    hyperparametres = Column(JSONB)
    features_utilisees = Column(JSONB)
    chemin_modele = Column(String(255))
    taille_mb = Column(Numeric(10,2))
    temps_entrainement_minutes = Column(Integer)
    dataset_version = Column(String(20))
    created_by = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
