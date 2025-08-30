from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.db.base_class import Base

class StatistiquesMatch(Base):
    __tablename__ = "statistiques_matchs"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False, unique=True)

    possession_dom = Column(Numeric(5, 2))
    possession_ext = Column(Numeric(5, 2))
    tirs_dom = Column(Integer)
    tirs_ext = Column(Integer)
    tirs_cadres_dom = Column(Integer)
    tirs_cadres_ext = Column(Integer)
    corners_dom = Column(Integer)
    corners_ext = Column(Integer)
    fautes_dom = Column(Integer)
    fautes_ext = Column(Integer)
    cartons_jaunes_dom = Column(Integer)
    cartons_jaunes_ext = Column(Integer)
    cartons_rouges_dom = Column(Integer)
    cartons_rouges_ext = Column(Integer)
    xg_dom = Column(Numeric(5, 2))
    xg_ext = Column(Numeric(5, 2))
    passes_reussies_dom = Column(Integer)
    passes_reussies_ext = Column(Integer)
    hors_jeux_dom = Column(Integer)
    hors_jeux_ext = Column(Integer)

    # ⚠️ Renommé: 'metadata' -> 'metadata_json' (pour éviter le nom réservé)
    metadata_json = Column(JSONB)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    match = relationship("Match", backref="stats")
