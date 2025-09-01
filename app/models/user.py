import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Role(str, enum.Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"

class StatutUtilisateur(str, enum.Enum):
    actif = "actif"
    suspendu = "suspendu"
    supprime = "supprime"

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)
    date_inscription = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    role = Column(Enum(Role, name="role_enum", native_enum=True), nullable=False, server_default=text("'user'"))
    statut = Column(Enum(StatutUtilisateur, name="statut_user_enum", native_enum=True), nullable=False, server_default=text("'actif'"))
    derniere_connexion = Column(TIMESTAMP, nullable=True)
    email_verifie = Column(Boolean, nullable=False, server_default=text("false"))
    double_auth_active = Column(Boolean, nullable=False, server_default=text("false"))
    secret_2fa = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    preferences = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # 🔗 Relation avec abonnements
    abonnements = relationship("Abonnement", back_populates="user")