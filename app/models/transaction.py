import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class MethodePaiement(str, enum.Enum):
    carte = "carte"
    paypal = "paypal"
    virement = "virement"
    crypto = "crypto"

class StatutPaiement(str, enum.Enum):
    en_attente = "en_attente"
    complete = "complete"
    echoue = "echoue"
    rembourse = "rembourse"

class TransactionPaiement(Base):
    __tablename__ = "transactions_paiements"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    abonnement_id = Column(Integer, ForeignKey("abonnements.id", ondelete="SET NULL"), nullable=True)
    montant = Column(Numeric(10,2), nullable=False)
    devise = Column(String(3), nullable=False, server_default=text("'EUR'"))
    methode_paiement = Column(Enum(MethodePaiement, name="methode_paiement_enum", native_enum=True), nullable=True)
    statut = Column(Enum(StatutPaiement, name="statut_paiement_enum", native_enum=True), nullable=False, server_default=text("'en_attente'"))
    provider_transaction_id = Column(String(255), nullable=True)
    provider_response = Column(JSONB, nullable=True)
    date_paiement = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
