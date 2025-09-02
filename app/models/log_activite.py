from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class LogActivite(Base):
    __tablename__ = "logs_activite"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # FK logique vers utilisateurs.id (non nécessaire pour inserts)
    type_action = Column(String(32), nullable=True)       # 'connexion','deconnexion','pronostic','consultation','commentaire','abonnement','api_call'
    endpoint = Column(String(255), nullable=True)
    methode = Column(String(10), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String, nullable=True)
    duree_ms = Column(Integer, nullable=True)
    code_reponse = Column(Integer, nullable=True)
    meta = Column("metadata", JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), index=True)
