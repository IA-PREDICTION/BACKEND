from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.db.base_class import Base

class Joueur(Base):
    __tablename__ = "joueurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100))
    equipe_id = Column(Integer, ForeignKey("equipes.id", ondelete="SET NULL"))
    position = Column(String(50))
    numero = Column(Integer)
    date_naissance = Column(Date)
    nationalite = Column(String(50))
    valeur_marchande = Column(Numeric(12, 2))
    api_id = Column(String(50))
    actif = Column(Boolean, nullable=False, server_default=text("true"))

    equipe = relationship("Equipe", backref="joueurs")
