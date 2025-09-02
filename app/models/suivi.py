from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy import text
from app.db.base_class import Base

class SuiviUtilisateur(Base):
    __tablename__ = "suivis_utilisateurs"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    following_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_follow_pair"),
    )
