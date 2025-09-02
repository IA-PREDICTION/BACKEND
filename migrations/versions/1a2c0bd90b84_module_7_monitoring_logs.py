"""module 7 monitoring & logs

Revision ID: 1a2c0bd90b84
Revises: module6_realtime_cache
Create Date: 2025-09-02 00:53:29.222342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2c0bd90b84'
down_revision: Union[str, Sequence[str], None] = 'module6_realtime_cache'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ENUMS idempotents
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_type_enum') THEN
            CREATE TYPE notification_type_enum AS ENUM (
                'match_debut','resultat_pronostic','nouveau_modele','abonnement_expire','promotion','suiveur_nouveau'
            );
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_channel_enum') THEN
            CREATE TYPE notification_channel_enum AS ENUM ('in_app','email','push','sms');
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_priority_enum') THEN
            CREATE TYPE notification_priority_enum AS ENUM ('basse','normale','haute');
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname='app_error_level_enum') THEN
            CREATE TYPE app_error_level_enum AS ENUM ('debug','info','warning','error','critical');
        END IF;
    END$$;
    """)

    # logs_activite
    op.create_table(
        "logs_activite",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("type_action", sa.String(32), nullable=True),
        sa.Column("endpoint", sa.String(255), nullable=True),
        sa.Column("methode", sa.String(10), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("duree_ms", sa.Integer(), nullable=True),
        sa.Column("code_reponse", sa.Integer(), nullable=True),
        sa.Column("metadata", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_logs_activite_user_created", "logs_activite", ["user_id", "created_at"])
    op.create_index("ix_logs_activite_type_created", "logs_activite", ["type_action", "created_at"])
    op.create_index("ix_logs_activite_created", "logs_activite", ["created_at"])

    # metriques_systeme
    op.create_table(
        "metriques_systeme",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("type_metrique", sa.String(64), nullable=False),
        sa.Column("valeur", sa.Numeric(10, 4), nullable=False),
        sa.Column("unite", sa.String(20), nullable=True),
        sa.Column("service", sa.String(50), nullable=True),
        sa.Column("tags", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("timestamp", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_metriques_type_ts", "metriques_systeme", ["type_metrique", "timestamp"])
    op.create_index("ix_metriques_service_ts", "metriques_systeme", ["service", "timestamp"])

    # notifications
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.Enum(name="notification_type_enum", native_enum=False), nullable=False),
        sa.Column("titre", sa.String(200), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("lue", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("canal", sa.Enum(name="notification_channel_enum", native_enum=False), server_default=sa.text("'in_app'"), nullable=False),
        sa.Column("priorite", sa.Enum(name="notification_priority_enum", native_enum=False), server_default=sa.text("'normale'"), nullable=False),
        sa.Column("donnees_contexte", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("date_envoi", sa.TIMESTAMP(), nullable=True),
        sa.Column("date_lecture", sa.TIMESTAMP(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_notifications_user_lue_created", "notifications", ["user_id", "lue", "created_at"])

    # erreurs_application
    op.create_table(
        "erreurs_application",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("service", sa.String(50), nullable=False),
        sa.Column("niveau", sa.Enum(name="app_error_level_enum", native_enum=False), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("stack_trace", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("context", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("resolved", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_erreurs_service_niveau_created", "erreurs_application", ["service", "niveau", "created_at"])
    op.create_index("ix_erreurs_resolved", "erreurs_application", ["resolved"])

def downgrade() -> None:
    op.drop_index("ix_erreurs_resolved", table_name="erreurs_application")
    op.drop_index("ix_erreurs_service_niveau_created", table_name="erreurs_application")
    op.drop_table("erreurs_application")

    op.drop_index("ix_notifications_user_lue_created", table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("ix_metriques_service_ts", table_name="metriques_systeme")
    op.drop_index("ix_metriques_type_ts", table_name="metriques_systeme")
    op.drop_table("metriques_systeme")

    op.drop_index("ix_logs_activite_created", table_name="logs_activite")
    op.drop_index("ix_logs_activite_type_created", table_name="logs_activite")
    op.drop_index("ix_logs_activite_user_created", table_name="logs_activite")
    op.drop_table("logs_activite")

    # Types ENUM: on ne les supprime que s’ils ne sont plus utilisés
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_type_enum') THEN
            DROP TYPE notification_type_enum;
        END IF;
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_channel_enum') THEN
            DROP TYPE notification_channel_enum;
        END IF;
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname='notification_priority_enum') THEN
            DROP TYPE notification_priority_enum;
        END IF;
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname='app_error_level_enum') THEN
            DROP TYPE app_error_level_enum;
        END IF;
    END$$;
    """)
