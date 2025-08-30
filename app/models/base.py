from app.db.base_class import Base
# Importons tous les modèles pour qu'Alembic voie les tables
from app.models.user import Utilisateur
from app.models.session_user import SessionUtilisateur
from app.models.plan import PlanAbonnement
from app.models.abonnement import Abonnement
from app.models.transaction import TransactionPaiement
