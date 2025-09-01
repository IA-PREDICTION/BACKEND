from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text, Index
from app.db.base_class import Base

class LogPrediction(Base):
    __tablename__ = "logs_predictions"

    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    modele_id = Column(Integer, ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False)
    input_features = Column(JSONB)
    output_raw = Column(JSONB)
    temps_inference_ms = Column(Integer)
    version_api = Column(String(20))
    erreur = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

Index("ix_logs_predictions_created", LogPrediction.created_at)
Index("ix_logs_predictions_modele_created", LogPrediction.modele_id, LogPrediction.created_at)
