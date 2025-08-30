from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Championnat(Base):
    __tablename__ = "championnats"

    id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String(100), nullable=False)
    pays = Column(String(50), nullable=True)
    niveau = Column(Integer, nullable=True)  # 1 = top league
    saison_actuelle = Column(String(20), nullable=True)
    logo_url = Column(String(255), nullable=True)
    api_id = Column(String(50), nullable=True, unique=False)
    actif = Column(Boolean, nullable=False, default=True)

    sport = relationship("Sport", back_populates="championnats")
    matchs = relationship("Match", back_populates="championnat", cascade="all, delete")
