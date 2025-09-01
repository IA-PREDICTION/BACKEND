from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.db.base_class import Base

class CoteBookmaker(Base):
    __tablename__ = "cotes_bookmakers"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False)
    bookmaker = Column(String(50), nullable=False)

    cote_dom = Column(Numeric(5, 2), nullable=False)
    cote_nul = Column(Numeric(5, 2), nullable=True)
    cote_ext = Column(Numeric(5, 2), nullable=False)

    cote_over_2_5 = Column(Numeric(5, 2), nullable=True)
    cote_under_2_5 = Column(Numeric(5, 2), nullable=True)
    cote_btts_oui = Column(Numeric(5, 2), nullable=True)
    cote_btts_non = Column(Numeric(5, 2), nullable=True)

    date_maj = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    match = relationship("Match", backref="cotes")

# index utile (match, bookmaker, date_maj)
Index("ix_cotes_match_book_date", CoteBookmaker.match_id, CoteBookmaker.bookmaker, CoteBookmaker.date_maj)
