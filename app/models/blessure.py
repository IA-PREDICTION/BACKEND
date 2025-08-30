import enum
from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, Enum, ForeignKey, Boolean
from sqlalchemy import text
from app.db.base_class import Base

class TypeIndispo(str, enum.Enum):
    blessure = "blessure"
    suspension = "suspension"
    autre = "autre"

class Gravite(str, enum.Enum):
    legere = "legere"
    moyenne = "moyenne"
    grave = "grave"

class BlessureSuspension(Base):
    __tablename__ = "blessures_suspensions"

    id = Column(Integer, primary_key=True)
    joueur_id = Column(Integer, ForeignKey("joueurs.id", ondelete="CASCADE"), nullable=False)
    equipe_id = Column(Integer, ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(TypeIndispo, name="type_indispo_enum", native_enum=True), nullable=False)
    gravite = Column(Enum(Gravite, name="gravite_enum", native_enum=True))
    date_debut = Column(Date, nullable=False)
    date_fin_prevue = Column(Date)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="SET NULL"))
    description = Column(Text)
    source = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
