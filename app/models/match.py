import enum
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy import Index
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.db.base_class import Base

class StatutMatch(str, enum.Enum):
    a_venir = "a_venir"
    en_cours = "en_cours"
    termine = "termine"
    reporte = "reporte"
    annule = "annule"

class Match(Base):
    __tablename__ = "matchs"

    id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    championnat_id = Column(Integer, ForeignKey("championnats.id", ondelete="CASCADE"), nullable=False)
    equipe_dom_id = Column(Integer, ForeignKey("equipes.id", ondelete="RESTRICT"), nullable=False)
    equipe_ext_id = Column(Integer, ForeignKey("equipes.id", ondelete="RESTRICT"), nullable=False)

    date_match = Column(TIMESTAMP, nullable=False)
    journee = Column(Integer, nullable=True)

    score_dom = Column(Integer, nullable=True)
    score_ext = Column(Integer, nullable=True)
    score_mi_temps_dom = Column(Integer, nullable=True)
    score_mi_temps_ext = Column(Integer, nullable=True)

    statut = Column(Enum(StatutMatch, name="statut_match_enum", native_enum=True), nullable=False, server_default=text("'a_venir'"))
    minute_actuelle = Column(Integer, nullable=True)
    api_id = Column(String(50), nullable=True)
    importance_match = Column(Integer, nullable=False, server_default=text("1"))  # 1-5
    diffusion_tv = Column(String(255), nullable=True)
    arbitre = Column(String(100), nullable=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    sport = relationship("Sport")
    championnat = relationship("Championnat", back_populates="matchs")
    equipe_dom = relationship("Equipe", foreign_keys=[equipe_dom_id], back_populates="matchs_domicile")
    equipe_ext = relationship("Equipe", foreign_keys=[equipe_ext_id], back_populates="matchs_exterieur")

# Indexes utiles
Index("ix_matchs_date_statut", Match.date_match, Match.statut)
Index("ix_matchs_pairing_date", Match.equipe_dom_id, Match.equipe_ext_id, Match.date_match)
