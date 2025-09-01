from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Boolean, DateTime, Enum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class PronosticUtilisateur(Base):
    __tablename__ = "pronostics_utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)

    choix_utilisateur = Column(Enum("1", "X", "2", name="choix_prono_enum"), nullable=True)
    score_predit_dom = Column(Integer, nullable=True)
    score_predit_ext = Column(Integer, nullable=True)
    mise_virtuelle = Column(Numeric(10, 2), default=0)
    cote = Column(Numeric(5, 2), nullable=True)

    date_pronostic = Column(DateTime(timezone=True), server_default=func.now())
    resultat = Column(Enum("gagne", "perdu", "en_attente", name="resultat_prono_enum"), server_default="en_attente")
    gains_virtuels = Column(Numeric(10, 2), default=0)
    partage_public = Column(Boolean, default=False)
    note_confiance = Column(Integer, nullable=True)  # 1-5 étoiles

    __table_args__ = (
        UniqueConstraint("user_id", "match_id", name="uq_user_match"),
    )

    # Relations
    user = relationship("Utilisateur", backref="pronostics")
    match = relationship("Match", backref="pronostics")
    prediction = relationship("Prediction", backref="user_pronostics")
