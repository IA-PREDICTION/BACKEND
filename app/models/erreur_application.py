import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class NiveauErreur(str, enum.Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"

class ErreurApplication(Base):
    __tablename__ = "erreurs_application"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(50), nullable=False, index=True)
    niveau = Column(Enum(NiveauErreur, name="app_error_level_enum", native_enum=True), nullable=False)
    message = Column(String, nullable=False)
    stack_trace = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True, index=True)   # FK logique
    context = Column(JSONB, nullable=True)
    resolved = Column(Boolean, nullable=False, server_default=text("false"), index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), index=True)
