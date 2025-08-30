from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    icone = Column(String(100), nullable=True)
    actif = Column(Boolean, nullable=False, default=True)

    championnats = relationship("Championnat", back_populates="sport", cascade="all, delete")
    equipes = relationship("Equipe", back_populates="sport", cascade="all, delete")
