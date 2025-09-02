from app.db.base_class import Base

# ⚠️ IMPORTER TOUS LES MODÈLES ICI (aucune logique, juste des imports)
from app.models.user import Utilisateur
from app.models.session_user import SessionUtilisateur

# Abonnements & plans (séparés)
from app.models.plan import PlanAbonnement
from app.models.abonnement import Abonnement  # + éventuel enum StatutAbonnement si défini dans ce fichier

# Paiements
from app.models.transaction import TransactionPaiement

# Données sportives
from app.models.sport import Sport
from app.models.championnat import Championnat
from app.models.equipe import Equipe
from app.models.match import Match
from app.models.cote import CoteBookmaker
from app.models.stat_match import StatistiquesMatch
from app.models.h2h import HistoriqueConfrontation
from app.models.joueur import Joueur
from app.models.blessure import BlessureSuspension

# IA / MLOps
from app.models.ml_model import ModeleIA
from app.models.feature_store_meta import FeatureStoreMeta
from app.models.features_engineering import FeaturesEngineering
from app.models.prediction import Prediction
from app.models.prediction_log import LogPrediction
from app.models.model_monitoring import ModelMonitoring

# Pronostics utilisateurs
from app.models.user_pronostic import PronosticUtilisateur

from app.models.commentaire import Commentaire
from app.models.reaction import Reaction
from app.models.suivi import SuiviUtilisateur

# Temps réel et cache 
from app.models.websocket_connection import WebsocketConnection
from app.models.cache_entry import CacheEntry
from app.models.queue_job import QueueJob

# Monitoring et logs 
from app.models.log_activite import LogActivite
from app.models.metrique_systeme import MetriqueSysteme
from app.models.notification import Notification
from app.models.erreur_application import ErreurApplication



