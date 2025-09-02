import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum, UniqueConstraint
from sqlalchemy import text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class TypeReaction(str, enum.Enum):
    like = "like"
    dislike = "dislike"
    love = "love"
    laugh = "laugh"
    surprised = "surprised"

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    commentaire_id = Column(Integer, ForeignKey("commentaires.id", ondelete="CASCADE"), nullable=True)
    pronostic_id = Column(Integer, ForeignKey("pronostics_utilisateurs.id", ondelete="CASCADE"), nullable=True)
    type = Column(Enum(TypeReaction, name="type_reaction_enum", native_enum=True), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    commentaire = relationship("Commentaire", back_populates="reactions")

    __table_args__ = (
        UniqueConstraint("user_id", "commentaire_id", name="uq_react_user_comment"),
        UniqueConstraint("user_id", "pronostic_id", name="uq_react_user_pronostic"),
    )
