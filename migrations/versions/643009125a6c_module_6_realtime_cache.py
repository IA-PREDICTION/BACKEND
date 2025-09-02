from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "module6_realtime_cache"
down_revision = "cf2120b366d1"  # <= adapte à ton dernier head actuel
branch_labels = None
depends_on = None

JOB_STATUS = ENUM(
    "en_attente", "en_cours", "complete", "echoue",
    name="queue_job_status_enum",
    create_type=False,  # ne pas recréer si déjà présent
)

def upgrade() -> None:
    # Types ENUM idempotents
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'queue_job_status_enum') THEN
            CREATE TYPE queue_job_status_enum AS ENUM ('en_attente','en_cours','complete','echoue');
        END IF;
    END$$;
    """)

    # websocket_connections
    op.create_table(
        "websocket_connections",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("connection_id", sa.String(100), nullable=False, unique=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("connected_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_ping", sa.TIMESTAMP(), nullable=True),
        sa.Column("rooms", sa.dialects.postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_ws_connection_id", "websocket_connections", ["connection_id"], unique=True)

    # cache_entries
    op.create_table(
        "cache_entries",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("cache_key", sa.String(255), nullable=False, unique=True),
        sa.Column("cache_value", sa.Text(), nullable=True),
        sa.Column("ttl_seconds", sa.Integer(), nullable=False),
        sa.Column("expire_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("tags", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_cache_expire_at", "cache_entries", ["expire_at"])
    op.create_index("ix_cache_key", "cache_entries", ["cache_key"], unique=True)

    # queue_jobs
    op.create_table(
        "queue_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("queue_name", sa.String(50), nullable=False),
        sa.Column("job_type", sa.String(100), nullable=False),
        sa.Column("payload", sa.dialects.postgresql.JSONB, nullable=False),
        sa.Column("statut", JOB_STATUS, nullable=False, server_default=sa.text("'en_attente'")),
        sa.Column("priorite", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("tentatives", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("max_tentatives", sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column("scheduled_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("started_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("completed_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_queue_jobs_qname_status_priority", "queue_jobs", ["queue_name", "statut", "priorite"])
    op.create_index("ix_queue_jobs_scheduled_at", "queue_jobs", ["scheduled_at"])

def downgrade() -> None:
    op.drop_index("ix_queue_jobs_scheduled_at", table_name="queue_jobs")
    op.drop_index("ix_queue_jobs_qname_status_priority", table_name="queue_jobs")
    op.drop_table("queue_jobs")

    op.drop_index("ix_cache_key", table_name="cache_entries")
    op.drop_index("ix_cache_expire_at", table_name="cache_entries")
    op.drop_table("cache_entries")

    op.drop_index("ix_ws_connection_id", table_name="websocket_connections")
    op.drop_table("websocket_connections")

    # drop type si plus utilisé
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'queue_job_status_enum') THEN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_attribute a
                JOIN pg_type t ON a.atttypid = t.oid
                WHERE t.typname = 'queue_job_status_enum' AND a.attisdropped = false
            ) THEN
                DROP TYPE queue_job_status_enum;
            END IF;
        END IF;
    END$$;
    """)
