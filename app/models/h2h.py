import enum
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class LieuH2H(str, enum.Enum):
    domicile_eq1 = "domicile_eq1"
    domicile_eq2 = "domicile_eq2"
    neutre = "neutre"

class HistoriqueConfrontation(Base):
    __tablename__ = "historiques_confrontations"

    id = Column(Integer, primary_key=True)
    equipe1_id = Column(Integer, ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False)
    equipe2_id = Column(Integer, ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    date_match = Column(TIMESTAMP, nullable=False)
    score_equipe1 = Column(Integer)
    score_equipe2 = Column(Integer)
    lieu = Column(Enum(LieuH2H, name="lieu_h2h_enum", native_enum=True))
    championnat_id = Column(Integer, ForeignKey("championnats.id", ondelete="SET NULL"))

    equipe1 = relationship("Equipe", foreign_keys=[equipe1_id])
    equipe2 = relationship("Equipe", foreign_keys=[equipe2_id])
    match = relationship("Match")
