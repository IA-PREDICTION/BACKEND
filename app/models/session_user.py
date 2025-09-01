import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Enum, ForeignKey
from sqlalchemy import text
from app.db.base_class import Base

class DeviceType(str, enum.Enum):
    web = "web"
    mobile = "mobile"
    tablet = "tablet"

class SessionUtilisateur(Base):
    __tablename__ = "sessions_utilisateurs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    token_session = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String, nullable=True)
    device_type = Column(Enum(DeviceType, name="device_type_enum", native_enum=True), nullable=True)
    expire_at = Column(TIMESTAMP, nullable=False)
    revoque = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
