from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Equipe(Base):
    __tablename__ = "equipes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    nom_court = Column(String(50), nullable=True)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    pays = Column(String(50), nullable=True)
    logo_url = Column(String(255), nullable=True)
    stade = Column(String(100), nullable=True)
    api_id = Column(String(50), nullable=True, unique=False)

    sport = relationship("Sport", back_populates="equipes")
    matchs_domicile = relationship("Match", foreign_keys="Match.equipe_dom_id", back_populates="equipe_dom")
    matchs_exterieur = relationship("Match", foreign_keys="Match.equipe_ext_id", back_populates="equipe_ext")
