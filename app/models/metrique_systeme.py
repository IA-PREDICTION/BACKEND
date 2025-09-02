from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class MetriqueSysteme(Base):
    __tablename__ = "metriques_systeme"

    id = Column(Integer, primary_key=True, index=True)
    type_metrique = Column(String(64), nullable=False, index=True)  # 'api_latency','prediction_time','db_query_time','cache_hit_rate','model_accuracy','websocket_connections'
    valeur = Column(Numeric(10, 4), nullable=False)
    unite = Column(String(20), nullable=True)
    service = Column(String(50), nullable=True, index=True)         # 'api','ml_service','feature_store'
    tags = Column(JSONB, nullable=True)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), index=True)
