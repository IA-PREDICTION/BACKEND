import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class JobStatus(str, enum.Enum):
    en_attente = "en_attente"
    en_cours = "en_cours"
    complete = "complete"
    echoue = "echoue"

class QueueJob(Base):
    __tablename__ = "queue_jobs"

    id = Column(Integer, primary_key=True, index=True)
    queue_name = Column(String(50), nullable=False, index=True)       # 'predictions', 'notifications', 'ingestion'
    job_type = Column(String(100), nullable=False)
    payload = Column(JSONB, nullable=False)
    statut = Column(Enum(JobStatus, name="queue_job_status_enum", native_enum=True),
                    nullable=False, server_default=text("'en_attente'"))
    priorite = Column(Integer, nullable=False, server_default=text("0"))
    tentatives = Column(Integer, nullable=False, server_default=text("0"))
    max_tentatives = Column(Integer, nullable=False, server_default=text("3"))
    scheduled_at = Column(TIMESTAMP, nullable=True, index=True)
    started_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
