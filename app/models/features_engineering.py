from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Numeric, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class FeaturesEngineering(Base):
    __tablename__ = "features_engineering"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    modele_id = Column(Integer, ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False)

    # Domicile
    forme_dom_5 = Column(Numeric(5,2))
    forme_dom_10 = Column(Numeric(5,2))
    moyenne_buts_marques_dom = Column(Numeric(5,2))
    moyenne_buts_encaisses_dom = Column(Numeric(5,2))
    clean_sheets_dom_5 = Column(Integer)

    # Extérieur
    forme_ext_5 = Column(Numeric(5,2))
    forme_ext_10 = Column(Numeric(5,2))
    moyenne_buts_marques_ext = Column(Numeric(5,2))
    moyenne_buts_encaisses_ext = Column(Numeric(5,2))
    clean_sheets_ext_5 = Column(Integer)

    # H2H
    h2h_victoires_dom = Column(Integer)
    h2h_nuls = Column(Integer)
    h2h_victoires_ext = Column(Integer)
    h2h_moyenne_buts = Column(Numeric(5,2))

    # Contexte
    jours_repos_dom = Column(Integer)
    jours_repos_ext = Column(Integer)
    nb_blesses_dom = Column(Integer)
    nb_blesses_ext = Column(Integer)
    importance_match_dom = Column(Integer)
    importance_match_ext = Column(Integer)

    # Avancées
    elo_rating_dom = Column(Numeric(8,2))
    elo_rating_ext = Column(Numeric(8,2))
    xg_rolling_dom = Column(Numeric(5,2))
    xg_rolling_ext = Column(Numeric(5,2))

    features_custom = Column(JSONB)
    version_pipeline = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

Index("ix_features_match_modele", FeaturesEngineering.match_id, FeaturesEngineering.modele_id)
