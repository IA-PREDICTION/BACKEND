import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from app.db.base_class import Base

class TypeNotif(str, enum.Enum):
    match_debut = "match_debut"
    resultat_pronostic = "resultat_pronostic"
    nouveau_modele = "nouveau_modele"
    abonnement_expire = "abonnement_expire"
    promotion = "promotion"
    suiveur_nouveau = "suiveur_nouveau"

class CanalNotif(str, enum.Enum):
    in_app = "in_app"
    email = "email"
    push = "push"
    sms = "sms"

class PrioriteNotif(str, enum.Enum):
    basse = "basse"
    normale = "normale"
    haute = "haute"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(TypeNotif, name="notification_type_enum", native_enum=True), nullable=False)
    titre = Column(String(200), nullable=False)
    message = Column(String, nullable=False)
    lue = Column(Boolean, nullable=False, server_default=text("false"), index=True)
    canal = Column(Enum(CanalNotif, name="notification_channel_enum", native_enum=True), nullable=False, server_default=text("'in_app'"))
    priorite = Column(Enum(PrioriteNotif, name="notification_priority_enum", native_enum=True), nullable=False, server_default=text("'normale'"))
    donnees_contexte = Column(JSONB, nullable=True)
    date_envoi = Column(TIMESTAMP, nullable=True)
    date_lecture = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), index=True)
