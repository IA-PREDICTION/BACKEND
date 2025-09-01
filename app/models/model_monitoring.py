from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class ModelMonitoring(Base):
    __tablename__ = "model_monitoring"

    id = Column(Integer, primary_key=True)
    modele_id = Column(Integer, ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False)
    date_evaluation = Column(Date, nullable=False)
    nb_predictions = Column(Integer)
    accuracy_reelle = Column(Numeric(5,2))
    drift_score = Column(Numeric(5,2))
    alertes = Column(JSONB)
    recommendations = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

Index("ix_monitoring_modele_date", ModelMonitoring.modele_id, ModelMonitoring.date_evaluation)
