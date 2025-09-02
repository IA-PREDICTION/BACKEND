"""module 8 ingestion & sync

Revision ID: 17696704dfe1
Revises: 1a2c0bd90b84
Create Date: 2025-09-02 01:21:34.136881
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "17696704dfe1"
down_revision: Union[str, Sequence[str], None] = "1a2c0bd90b84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ---------------------------
    # 1) Ingestion: sources + logs
    # ---------------------------
    op.create_table(
        "sources_donnees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nom", sa.String(length=100), nullable=False),
        sa.Column(
            "type",
            sa.Enum("api", "scraping", "manual", name="type_source_enum"),
            nullable=False,
        ),
        sa.Column("url_base", sa.String(length=255), nullable=True),
        sa.Column("api_key_encrypted", sa.String(length=255), nullable=True),
        sa.Column("frequence_maj_minutes", sa.Integer(), nullable=True),
        sa.Column("derniere_synchro", sa.TIMESTAMP(), nullable=True),
        sa.Column("prochaine_synchro", sa.TIMESTAMP(), nullable=True),
        sa.Column(
            "statut",
            sa.Enum("actif", "pause", "erreur", name="statut_source_enum"),
            server_default=sa.text("'actif'"),
            nullable=False,
        ),
        sa.Column("configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("rate_limit_par_heure", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index(op.f("ix_public_sources_donnees_id"), "sources_donnees", ["id"], unique=False, schema="public")

    op.create_table(
        "logs_ingestion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("type_donnees", sa.String(length=50), nullable=True),
        sa.Column("nb_enregistrements", sa.Integer(), nullable=True),
        sa.Column("nb_nouveaux", sa.Integer(), nullable=True),
        sa.Column("nb_modifies", sa.Integer(), nullable=True),
        sa.Column("nb_erreurs", sa.Integer(), nullable=True),
        sa.Column("duree_secondes", sa.Integer(), nullable=True),
        sa.Column(
            "statut",
            sa.Enum("succes", "partiel", "echec", name="statut_ingestion_enum"),
            nullable=True,
        ),
        sa.Column("erreurs", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["public.sources_donnees.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index(op.f("ix_public_logs_ingestion_id"), "logs_ingestion", ["id"], unique=False, schema="public")

    # ---------------------------
    # 2) FK abonnements -> plans_abonnement (sécurité)
    # ---------------------------
    op.create_foreign_key(None, "abonnements", "plans_abonnement", ["plan_id"], ["id"], ondelete="RESTRICT")

    # ---------------------------
    # 3) Cache: index/uniques
    # ---------------------------
    op.drop_constraint(op.f("cache_entries_cache_key_key"), "cache_entries", type_="unique")
    op.drop_index(op.f("ix_cache_expire_at"), table_name="cache_entries")
    op.drop_index(op.f("ix_cache_key"), table_name="cache_entries")
    op.create_index(op.f("ix_cache_entries_cache_key"), "cache_entries", ["cache_key"], unique=True)
    op.create_index(op.f("ix_cache_entries_expire_at"), "cache_entries", ["expire_at"], unique=False)
    op.create_index(op.f("ix_cache_entries_id"), "cache_entries", ["id"], unique=False)

    # ---------------------------
    # 4) Commentaires: index compactés
    # ---------------------------
    op.drop_index(op.f("ix_commentaires_match_id_created_at"), table_name="commentaires")
    op.drop_index(op.f("ix_commentaires_user_id_created_at"), table_name="commentaires")
    op.create_index("ix_commentaires_match_created", "commentaires", ["match_id", "created_at"], unique=False)
    op.create_index("ix_commentaires_user_created", "commentaires", ["user_id", "created_at"], unique=False)

    # ---------------------------
    # 5) ENUM migrations (avec USING)
    # ---------------------------

    # erreurs_application.niveau -> ENUM
    app_error_level_enum = postgresql.ENUM(
        "debug", "info", "warning", "error", "critical",
        name="app_error_level_enum",
        create_type=False,
    )
    app_error_level_enum.create(op.get_bind(), checkfirst=True)

    # normaliser valeurs existantes (tout ce qui n'est pas attendu -> 'info')
    op.execute(
        """
        UPDATE erreurs_application
        SET niveau = CASE
            WHEN niveau IN ('debug','info','warning','error','critical') THEN niveau
            ELSE 'info'
        END
        """
    )

    op.alter_column(
        "erreurs_application",
        "niveau",
        existing_type=sa.VARCHAR(),
        type_=app_error_level_enum,
        postgresql_using="niveau::app_error_level_enum",
        existing_nullable=False,
        server_default=sa.text("'info'"),
    )

    # notifications.* -> ENUMS
    notification_type_enum = postgresql.ENUM(
        "match_debut",
        "resultat_pronostic",
        "nouveau_modele",
        "abonnement_expire",
        "promotion",
        "suiveur_nouveau",
        name="notification_type_enum",
        create_type=False,
    )
    notification_type_enum.create(op.get_bind(), checkfirst=True)

    notification_channel_enum = postgresql.ENUM(
        "in_app", "email", "push", "sms",
        name="notification_channel_enum",
        create_type=False,
    )
    notification_channel_enum.create(op.get_bind(), checkfirst=True)

    notification_priority_enum = postgresql.ENUM(
        "basse", "normale", "haute",
        name="notification_priority_enum",
        create_type=False,
    )
    notification_priority_enum.create(op.get_bind(), checkfirst=True)

    # normalisation préventive
    op.execute(
        """
        UPDATE notifications
        SET type = CASE
            WHEN type IN ('match_debut','resultat_pronostic','nouveau_modele','abonnement_expire','promotion','suiveur_nouveau') THEN type
            ELSE 'promotion'
        END
        """
    )
    op.execute(
        """
        UPDATE notifications
        SET canal = CASE
            WHEN canal IN ('in_app','email','push','sms') THEN canal
            ELSE 'in_app'
        END
        """
    )
    op.execute(
        """
        UPDATE notifications
        SET priorite = CASE
            WHEN priorite IN ('basse','normale','haute') THEN priorite
            ELSE 'normale'
        END
        """
    )

    op.alter_column(
        "notifications",
        "type",
        existing_type=sa.VARCHAR(),
        type_=notification_type_enum,
        postgresql_using="type::notification_type_enum",
        existing_nullable=False,
    )

    # canal : il faut D'ABORD drop le default varchar
    op.execute("ALTER TABLE notifications ALTER COLUMN canal DROP DEFAULT")

    op.alter_column(
        "notifications",
        "canal",
        existing_type=sa.VARCHAR(),
        type_=notification_channel_enum,
        postgresql_using="canal::notification_channel_enum",
        existing_nullable=False,
    )

    # puis on remet un default typé ENUM
    op.execute("ALTER TABLE notifications ALTER COLUMN canal SET DEFAULT 'in_app'::notification_channel_enum")

    # priorite : idem, drop default puis alter puis set default
    op.execute("ALTER TABLE notifications ALTER COLUMN priorite DROP DEFAULT")

    op.alter_column(
        "notifications",
        "priorite",
        existing_type=sa.VARCHAR(),
        type_=notification_priority_enum,
        postgresql_using="priorite::notification_priority_enum",
        existing_nullable=False,
    )
    op.execute("ALTER TABLE notifications ALTER COLUMN priorite SET DEFAULT 'normale'::notification_priority_enum")
    # ---------------------------
    # 6) Index divers (logs/metrics/notifications/plans/queue/ws)
    # ---------------------------
    op.drop_index(op.f("ix_erreurs_resolved"), table_name="erreurs_application")
    op.drop_index(op.f("ix_erreurs_service_niveau_created"), table_name="erreurs_application")
    op.create_index(op.f("ix_erreurs_application_created_at"), "erreurs_application", ["created_at"], unique=False)
    op.create_index(op.f("ix_erreurs_application_id"), "erreurs_application", ["id"], unique=False)
    op.create_index(op.f("ix_erreurs_application_resolved"), "erreurs_application", ["resolved"], unique=False)
    op.create_index(op.f("ix_erreurs_application_service"), "erreurs_application", ["service"], unique=False)
    op.create_index(op.f("ix_erreurs_application_user_id"), "erreurs_application", ["user_id"], unique=False)

    op.drop_index(op.f("ix_logs_activite_created"), table_name="logs_activite")
    op.drop_index(op.f("ix_logs_activite_type_created"), table_name="logs_activite")
    op.drop_index(op.f("ix_logs_activite_user_created"), table_name="logs_activite")
    op.create_index(op.f("ix_logs_activite_created_at"), "logs_activite", ["created_at"], unique=False)
    op.create_index(op.f("ix_logs_activite_id"), "logs_activite", ["id"], unique=False)
    op.create_index(op.f("ix_logs_activite_user_id"), "logs_activite", ["user_id"], unique=False)

    op.drop_index(op.f("ix_metriques_service_ts"), table_name="metriques_systeme")
    op.drop_index(op.f("ix_metriques_type_ts"), table_name="metriques_systeme")
    op.create_index(op.f("ix_metriques_systeme_id"), "metriques_systeme", ["id"], unique=False)
    op.create_index(op.f("ix_metriques_systeme_service"), "metriques_systeme", ["service"], unique=False)
    op.create_index(op.f("ix_metriques_systeme_timestamp"), "metriques_systeme", ["timestamp"], unique=False)
    op.create_index(op.f("ix_metriques_systeme_type_metrique"), "metriques_systeme", ["type_metrique"], unique=False)

    op.drop_index(op.f("ix_notifications_user_lue_created"), table_name="notifications")
    op.create_index(op.f("ix_notifications_created_at"), "notifications", ["created_at"], unique=False)
    op.create_index(op.f("ix_notifications_id"), "notifications", ["id"], unique=False)
    op.create_index(op.f("ix_notifications_lue"), "notifications", ["lue"], unique=False)
    op.create_index(op.f("ix_notifications_user_id"), "notifications", ["user_id"], unique=False)

    # plans_abonnement: rendre NOT NULL certains bool/int (aligné avec ton modèle)
    op.alter_column("plans_abonnement", "acces_stats_avancees", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "acces_predictions_ia", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("true"))
    op.alter_column("plans_abonnement", "acces_historique_complet", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "acces_api", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "priority_support", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "periode_essai_jours", existing_type=sa.INTEGER(), nullable=False, existing_server_default=sa.text("0"))
    op.alter_column("plans_abonnement", "actif", existing_type=sa.BOOLEAN(), nullable=False, existing_server_default=sa.text("true"))
    op.alter_column("plans_abonnement", "ordre_affichage", existing_type=sa.INTEGER(), nullable=False, existing_server_default=sa.text("0"))

    op.drop_index(op.f("ix_queue_jobs_qname_status_priority"), table_name="queue_jobs")
    op.create_index(op.f("ix_queue_jobs_id"), "queue_jobs", ["id"], unique=False)
    op.create_index(op.f("ix_queue_jobs_queue_name"), "queue_jobs", ["queue_name"], unique=False)

    op.drop_index(op.f("ix_ws_connection_id"), table_name="websocket_connections")
    op.drop_constraint(op.f("websocket_connections_connection_id_key"), "websocket_connections", type_="unique")
    op.create_index(op.f("ix_websocket_connections_connection_id"), "websocket_connections", ["connection_id"], unique=True)
    op.create_index(op.f("ix_websocket_connections_id"), "websocket_connections", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    # Revert websocket
    op.drop_index(op.f("ix_websocket_connections_id"), table_name="websocket_connections")
    op.drop_index(op.f("ix_websocket_connections_connection_id"), table_name="websocket_connections")
    op.create_unique_constraint(
        op.f("websocket_connections_connection_id_key"),
        "websocket_connections",
        ["connection_id"],
        postgresql_nulls_not_distinct=False,
    )
    op.create_index(op.f("ix_ws_connection_id"), "websocket_connections", ["connection_id"], unique=True)

    # Revert queue_jobs
    op.drop_index(op.f("ix_queue_jobs_queue_name"), table_name="queue_jobs")
    op.drop_index(op.f("ix_queue_jobs_id"), table_name="queue_jobs")
    op.create_index(op.f("ix_queue_jobs_qname_status_priority"), "queue_jobs", ["queue_name", "statut", "priorite"], unique=False)

    # Revert plans_abonnement nullability
    op.alter_column("plans_abonnement", "ordre_affichage", existing_type=sa.INTEGER(), nullable=True, existing_server_default=sa.text("0"))
    op.alter_column("plans_abonnement", "actif", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("true"))
    op.alter_column("plans_abonnement", "periode_essai_jours", existing_type=sa.INTEGER(), nullable=True, existing_server_default=sa.text("0"))
    op.alter_column("plans_abonnement", "priority_support", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "acces_api", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "acces_historique_complet", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("false"))
    op.alter_column("plans_abonnement", "acces_predictions_ia", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("true"))
    op.alter_column("plans_abonnement", "acces_stats_avancees", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("false"))

    # Revert notifications indexes
    op.drop_index(op.f("ix_notifications_user_id"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_lue"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_id"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_created_at"), table_name="notifications")
    op.create_index(op.f("ix_notifications_user_lue_created"), "notifications", ["user_id", "lue", "created_at"], unique=False)

    # notifications.* ENUM -> VARCHAR
    op.alter_column(
        "notifications",
        "priorite",
        existing_type=sa.Enum("basse", "normale", "haute", name="notification_priority_enum"),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        server_default=sa.text("'normale'::character varying"),
        postgresql_using="priorite::text",
    )
    op.alter_column(
        "notifications",
        "canal",
        existing_type=sa.Enum("in_app", "email", "push", "sms", name="notification_channel_enum"),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        server_default=sa.text("'in_app'::character varying"),
        postgresql_using="canal::text",
    )
    op.alter_column(
        "notifications",
        "type",
        existing_type=sa.Enum(
            "match_debut",
            "resultat_pronostic",
            "nouveau_modele",
            "abonnement_expire",
            "promotion",
            "suiveur_nouveau",
            name="notification_type_enum",
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="type::text",
    )

    # Revert metriques_systeme indexes
    op.drop_index(op.f("ix_metriques_systeme_type_metrique"), table_name="metriques_systeme")
    op.drop_index(op.f("ix_metriques_systeme_timestamp"), table_name="metriques_systeme")
    op.drop_index(op.f("ix_metriques_systeme_service"), table_name="metriques_systeme")
    op.drop_index(op.f("ix_metriques_systeme_id"), table_name="metriques_systeme")
    op.create_index(op.f("ix_metriques_type_ts"), "metriques_systeme", ["type_metrique", "timestamp"], unique=False)
    op.create_index(op.f("ix_metriques_service_ts"), "metriques_systeme", ["service", "timestamp"], unique=False)

    # Revert logs_activite indexes
    op.drop_index(op.f("ix_logs_activite_user_id"), table_name="logs_activite")
    op.drop_index(op.f("ix_logs_activite_id"), table_name="logs_activite")
    op.drop_index(op.f("ix_logs_activite_created_at"), table_name="logs_activite")
    op.create_index(op.f("ix_logs_activite_user_created"), "logs_activite", ["user_id", "created_at"], unique=False)
    op.create_index(op.f("ix_logs_activite_type_created"), "logs_activite", ["type_action", "created_at"], unique=False)
    op.create_index(op.f("ix_logs_activite_created"), "logs_activite", ["created_at"], unique=False)

    # Revert erreurs_application indexes
    op.drop_index(op.f("ix_erreurs_application_user_id"), table_name="erreurs_application")
    op.drop_index(op.f("ix_erreurs_application_service"), table_name="erreurs_application")
    op.drop_index(op.f("ix_erreurs_application_resolved"), table_name="erreurs_application")
    op.drop_index(op.f("ix_erreurs_application_id"), table_name="erreurs_application")
    op.drop_index(op.f("ix_erreurs_application_created_at"), table_name="erreurs_application")
    op.create_index(op.f("ix_erreurs_service_niveau_created"), "erreurs_application", ["service", "niveau", "created_at"], unique=False)
    op.create_index(op.f("ix_erreurs_resolved"), "erreurs_application", ["resolved"], unique=False)

    # erreurs_application.niveau ENUM -> VARCHAR
    op.alter_column(
        "erreurs_application",
        "niveau",
        existing_type=sa.Enum("debug", "info", "warning", "error", "critical", name="app_error_level_enum"),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="niveau::text",
    )

    # Revert commentaires indexes
    op.drop_index("ix_commentaires_user_created", table_name="commentaires")
    op.drop_index("ix_commentaires_match_created", table_name="commentaires")
    op.create_index(op.f("ix_commentaires_user_id_created_at"), "commentaires", ["user_id", "created_at"], unique=False)
    op.create_index(op.f("ix_commentaires_match_id_created_at"), "commentaires", ["match_id", "created_at"], unique=False)

    # Revert cache indexes & unique
    op.drop_index(op.f("ix_cache_entries_id"), table_name="cache_entries")
    op.drop_index(op.f("ix_cache_entries_expire_at"), table_name="cache_entries")
    op.drop_index(op.f("ix_cache_entries_cache_key"), table_name="cache_entries")
    op.create_index(op.f("ix_cache_key"), "cache_entries", ["cache_key"], unique=True)
    op.create_index(op.f("ix_cache_expire_at"), "cache_entries", ["expire_at"], unique=False)
    op.create_unique_constraint(op.f("cache_entries_cache_key_key"), "cache_entries", ["cache_key"], postgresql_nulls_not_distinct=False)

    # Revert FK abonnements
    op.drop_constraint(None, "abonnements", type_="foreignkey")

    # Drop logs_ingestion / sources_donnees
    op.drop_index(op.f("ix_public_logs_ingestion_id"), table_name="logs_ingestion", schema="public")
    op.drop_table("logs_ingestion", schema="public")
    op.drop_index(op.f("ix_public_sources_donnees_id"), table_name="sources_donnees", schema="public")
    op.drop_table("sources_donnees", schema="public")

    # Drop ENUM types créés explicitement (après conversion en VARCHAR)
    bind = op.get_bind()
    # ceux utilisés par notifications
    try:
        postgresql.ENUM(name="notification_priority_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name="notification_channel_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name="notification_type_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    # erreurs_application
    try:
        postgresql.ENUM(name="app_error_level_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    # ingestion enums (créés avec les tables) — on tente de les supprimer si plus référencés
    try:
        postgresql.ENUM(name="statut_ingestion_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name="statut_source_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name="type_source_enum").drop(bind=bind, checkfirst=True)
    except Exception:
        pass
