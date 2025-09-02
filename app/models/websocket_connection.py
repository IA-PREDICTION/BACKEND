from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class WebsocketConnection(Base):
    __tablename__ = "websocket_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    connection_id = Column(String(100), unique=True, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    connected_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    last_ping = Column(TIMESTAMP, nullable=True)
    rooms = Column(JSONB, nullable=True)  # ex: ["match_123", "global_notifications"]
