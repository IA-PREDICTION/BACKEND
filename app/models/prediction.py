from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base
from app.models.ml_model import TypePrediction

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    modele_id = Column(Integer, ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False)
    type_prediction = Column(Enum(TypePrediction, name="type_prediction_enum", native_enum=True))

    # Match result
    proba_victoire_dom = Column(Numeric(5,2))
    proba_nul = Column(Numeric(5,2))
    proba_victoire_ext = Column(Numeric(5,2))
    prediction_finale =  Column(String(16))  # assez pour "BTTS_OUI"/"BTTS_NON"/"UNDER"/"OVER"/"1-0"
    confidence = Column(Numeric(5,2))

    # Score exact
    score_predit_dom = Column(Integer)
    score_predit_ext = Column(Integer)

    # Over/Under
    total_buts_predit = Column(Numeric(5,2))
    proba_over_2_5 = Column(Numeric(5,2))
    proba_under_2_5 = Column(Numeric(5,2))

    # BTTS
    proba_btts_oui = Column(Numeric(5,2))
    proba_btts_non = Column(Numeric(5,2))

    # Meta
    features_importance = Column(JSONB)
    shap_values = Column(JSONB)
    date_prediction = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    batch_id = Column(String(50))
    temps_calcul_ms = Column(Integer)

Index("ix_predictions_match_modele_type", Prediction.match_id, Prediction.modele_id, Prediction.type_prediction)
Index("ix_predictions_date", Prediction.date_prediction)
