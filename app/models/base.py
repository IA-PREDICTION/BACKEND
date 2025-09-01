from app.db.base_class import Base
# Importons tous les modèles pour qu'Alembic voie les tables
from app.models.user import Utilisateur
from app.models.session_user import SessionUtilisateur
from app.models.plan import PlanAbonnement
from app.models.abonnement import Abonnement
from app.models.transaction import TransactionPaiement
from app.models.sport import Sport
from app.models.championnat import Championnat
from app.models.equipe import Equipe
from app.models.match import Match
from app.models.cote import CoteBookmaker
from app.models.stat_match import StatistiquesMatch
from app.models.h2h import HistoriqueConfrontation
from app.models.joueur import Joueur
from app.models.blessure import BlessureSuspension