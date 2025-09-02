import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, Enum, Index
from sqlalchemy import text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class StatutComment(str, enum.Enum):
    visible = "visible"
    modere = "modere"
    supprime = "supprime"

class Commentaire(Base):
    __tablename__ = "commentaires"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="SET NULL"), nullable=True)
    pronostic_id = Column(Integer, ForeignKey("pronostics_utilisateurs.id", ondelete="SET NULL"), nullable=True)
    parent_id = Column(Integer, ForeignKey("commentaires.id", ondelete="CASCADE"), nullable=True)

    contenu = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False, server_default=text("0"))
    signalements = Column(Integer, nullable=False, server_default=text("0"))
    statut = Column(Enum(StatutComment, name="statut_comment_enum", native_enum=True), nullable=False, server_default=text("'visible'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # relations
    user = relationship("Utilisateur")
    parent = relationship("Commentaire", remote_side=[id])
    reactions = relationship("Reaction", cascade="all, delete-orphan", back_populates="commentaire")

# Indexes utiles
Index("ix_commentaires_match_created", Commentaire.match_id, Commentaire.created_at)
Index("ix_commentaires_user_created", Commentaire.user_id, Commentaire.created_at)
