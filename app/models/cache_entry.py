from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from sqlalchemy import text
from app.db.base_class import Base

class CacheEntry(Base):
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, nullable=False, index=True)
    cache_value = Column(TEXT, nullable=True)  # on stocke du texte (peut contenir du JSON sérialisé)
    ttl_seconds = Column(Integer, nullable=False)
    expire_at = Column(TIMESTAMP, nullable=False, index=True)
    tags = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
