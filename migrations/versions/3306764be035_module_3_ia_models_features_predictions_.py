"""module 3 IA (models/features/predictions/logs/monitoring)

Revision ID: 3306764be035
Revises: c3d019f7b973
Create Date: 2025-09-01 20:09:09.471833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3306764be035'
down_revision: Union[str, Sequence[str], None] = 'c3d019f7b973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(insp, name: str) -> bool:
    return name in insp.get_table_names()

def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # --- ENUMS (protégés) ---
    # NB: si ces types existent déjà (créés par une autre migration), on n'essaie pas de les recréer.
    try:
        sa.Enum(
            "entrainement", "validation", "production", "archive",
            name="statut_modele_enum", create_type=False
        ).create(bind, checkfirst=True)
    except Exception:
        pass

    try:
        sa.Enum(
            "match_result", "score_exact", "over_under", "both_teams_score",
            name="type_prediction_enum", create_type=False
        ).create(bind, checkfirst=True)
    except Exception:
        pass

    # --- feature_store_metadata ---
    if not _has_table(insp, "feature_store_metadata"):
        op.create_table(
            "feature_store_metadata",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("nom_feature", sa.String(100), nullable=False),
            sa.Column("description", sa.Text()),
            sa.Column("type_donnee", sa.String(50)),
            sa.Column("source", sa.String(100)),
            sa.Column("formule_calcul", sa.Text()),
            sa.Column("importance_moyenne", sa.Numeric(5, 2)),
            sa.Column("statut", sa.String(20), server_default=sa.text("'actif'")),
            sa.Column("version", sa.String(20)),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.UniqueConstraint("nom_feature"),
        )

    # --- modeles_ia ---
    if not _has_table(insp, "modeles_ia"):
        op.create_table(
            "modeles_ia",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("nom", sa.String(100), nullable=False),
            sa.Column("version", sa.String(20), nullable=False),
            sa.Column("sport_id", sa.Integer(), sa.ForeignKey("sports.id", ondelete="CASCADE"), nullable=False),
            sa.Column("type_prediction", sa.Enum(name="type_prediction_enum", create_type=False)),
            sa.Column("algorithme", sa.String(50)),
            sa.Column("accuracy", sa.Numeric(5, 2)),
            sa.Column("precision_score", sa.Numeric(5, 2)),
            sa.Column("recall_score", sa.Numeric(5, 2)),
            sa.Column("f1_score", sa.Numeric(5, 2)),
            sa.Column("date_entrainement", sa.TIMESTAMP(), nullable=False),
            sa.Column("date_deploiement", sa.TIMESTAMP()),
            sa.Column("statut", sa.Enum(name="statut_modele_enum", create_type=False), server_default=sa.text("'entrainement'")),
            sa.Column("hyperparametres", sa.dialects.postgresql.JSONB()),
            sa.Column("features_utilisees", sa.dialects.postgresql.JSONB()),
            sa.Column("chemin_modele", sa.String(255)),
            sa.Column("taille_mb", sa.Numeric(10, 2)),
            sa.Column("temps_entrainement_minutes", sa.Integer()),
            sa.Column("dataset_version", sa.String(20)),
            sa.Column("created_by", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="SET NULL")),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index(
            "ix_modeles_ia_sport_type_statut",
            "modeles_ia", ["sport_id", "type_prediction", "statut"], unique=False
        )

    # --- features_engineering ---
    if not _has_table(insp, "features_engineering"):
        op.create_table(
            "features_engineering",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("modele_id", sa.Integer(), sa.ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False),
            sa.Column("forme_dom_5", sa.Numeric(5, 2)),
            sa.Column("forme_dom_10", sa.Numeric(5, 2)),
            sa.Column("moyenne_buts_marques_dom", sa.Numeric(5, 2)),
            sa.Column("moyenne_buts_encaisses_dom", sa.Numeric(5, 2)),
            sa.Column("clean_sheets_dom_5", sa.Integer()),
            sa.Column("forme_ext_5", sa.Numeric(5, 2)),
            sa.Column("forme_ext_10", sa.Numeric(5, 2)),
            sa.Column("moyenne_buts_marques_ext", sa.Numeric(5, 2)),
            sa.Column("moyenne_buts_encaisses_ext", sa.Numeric(5, 2)),
            sa.Column("clean_sheets_ext_5", sa.Integer()),
            sa.Column("h2h_victoires_dom", sa.Integer()),
            sa.Column("h2h_nuls", sa.Integer()),
            sa.Column("h2h_victoires_ext", sa.Integer()),
            sa.Column("h2h_moyenne_buts", sa.Numeric(5, 2)),
            sa.Column("jours_repos_dom", sa.Integer()),
            sa.Column("jours_repos_ext", sa.Integer()),
            sa.Column("nb_blesses_dom", sa.Integer()),
            sa.Column("nb_blesses_ext", sa.Integer()),
            sa.Column("importance_match_dom", sa.Integer()),
            sa.Column("importance_match_ext", sa.Integer()),
            sa.Column("elo_rating_dom", sa.Numeric(8, 2)),
            sa.Column("elo_rating_ext", sa.Numeric(8, 2)),
            sa.Column("xg_rolling_dom", sa.Numeric(5, 2)),
            sa.Column("xg_rolling_ext", sa.Numeric(5, 2)),
            sa.Column("features_custom", sa.dialects.postgresql.JSONB()),
            sa.Column("version_pipeline", sa.String(20)),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index(
            "ix_features_engineering_match_modele",
            "features_engineering", ["match_id", "modele_id"], unique=False
        )

    # --- predictions ---
    if not _has_table(insp, "predictions"):
        # ATTENTION : si tu as déjà eu l'erreur "varchar(1) trop court", on évite un Enum strict ici
        op.create_table(
            "predictions",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("modele_id", sa.Integer(), sa.ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False),
            sa.Column("type_prediction", sa.Enum(name="type_prediction_enum", create_type=False)),
            sa.Column("proba_victoire_dom", sa.Numeric(5, 2)),
            sa.Column("proba_nul", sa.Numeric(5, 2)),
            sa.Column("proba_victoire_ext", sa.Numeric(5, 2)),
            sa.Column("prediction_finale", sa.String(10)),  # '1','X','2','OVER','UNDER', etc.
            sa.Column("confidence", sa.Numeric(5, 2)),
            sa.Column("score_predit_dom", sa.Integer()),
            sa.Column("score_predit_ext", sa.Integer()),
            sa.Column("total_buts_predit", sa.Numeric(5, 2)),
            sa.Column("proba_over_2_5", sa.Numeric(5, 2)),
            sa.Column("proba_under_2_5", sa.Numeric(5, 2)),
            sa.Column("proba_btts_oui", sa.Numeric(5, 2)),
            sa.Column("proba_btts_non", sa.Numeric(5, 2)),
            sa.Column("features_importance", sa.dialects.postgresql.JSONB()),
            sa.Column("shap_values", sa.dialects.postgresql.JSONB()),
            sa.Column("date_prediction", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.Column("batch_id", sa.String(50)),
            sa.Column("temps_calcul_ms", sa.Integer()),
        )
        op.create_index(
            "ix_predictions_match_modele_type",
            "predictions", ["match_id", "modele_id", "type_prediction"], unique=False
        )
        op.create_index(
            "ix_predictions_date",
            "predictions", ["date_prediction"], unique=False
        )

    # --- logs_predictions ---
    if not _has_table(insp, "logs_predictions"):
        op.create_table(
            "logs_predictions",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("prediction_id", sa.Integer(), sa.ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("modele_id", sa.Integer(), sa.ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False),
            sa.Column("input_features", sa.dialects.postgresql.JSONB()),
            sa.Column("output_raw", sa.dialects.postgresql.JSONB()),
            sa.Column("temps_inference_ms", sa.Integer()),
            sa.Column("version_api", sa.String(20)),
            sa.Column("erreur", sa.Text()),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index(
            "ix_logs_predictions_created_at",
            "logs_predictions", ["created_at"], unique=False
        )
        op.create_index(
            "ix_logs_predictions_modele_created",
            "logs_predictions", ["modele_id", "created_at"], unique=False
        )

    # --- model_monitoring ---
    if not _has_table(insp, "model_monitoring"):
        op.create_table(
            "model_monitoring",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("modele_id", sa.Integer(), sa.ForeignKey("modeles_ia.id", ondelete="CASCADE"), nullable=False),
            sa.Column("date_evaluation", sa.Date(), nullable=False),
            sa.Column("nb_predictions", sa.Integer()),
            sa.Column("accuracy_reelle", sa.Numeric(5, 2)),
            sa.Column("drift_score", sa.Numeric(5, 2)),
            sa.Column("alertes", sa.dialects.postgresql.JSONB()),
            sa.Column("recommendations", sa.Text()),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        op.create_index(
            "ix_model_monitoring_modele_date",
            "model_monitoring", ["modele_id", "date_evaluation"], unique=False
        )


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if _has_table(insp, "model_monitoring"):
        op.drop_index("ix_model_monitoring_modele_date", table_name="model_monitoring")
        op.drop_table("model_monitoring")

    if _has_table(insp, "logs_predictions"):
        op.drop_index("ix_logs_predictions_modele_created", table_name="logs_predictions")
        op.drop_index("ix_logs_predictions_created_at", table_name="logs_predictions")
        op.drop_table("logs_predictions")

    if _has_table(insp, "predictions"):
        op.drop_index("ix_predictions_date", table_name="predictions")
        op.drop_index("ix_predictions_match_modele_type", table_name="predictions")
        op.drop_table("predictions")

    if _has_table(insp, "features_engineering"):
        op.drop_index("ix_features_engineering_match_modele", table_name="features_engineering")
        op.drop_table("features_engineering")

    if _has_table(insp, "modeles_ia"):
        op.drop_index("ix_modeles_ia_sport_type_statut", table_name="modeles_ia")
        op.drop_table("modeles_ia")

    if _has_table(insp, "feature_store_metadata"):
        op.drop_table("feature_store_metadata")

    # On laisse les ENUM si utilisés ailleurs
    try:
        sa.Enum(name="type_prediction_enum").drop(bind, checkfirst=True)
        sa.Enum(name="statut_modele_enum").drop(bind, checkfirst=True)
    except Exception:
        pass
