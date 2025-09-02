from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "cf2120b366d1"
down_revision = "42224107aeb4"
branch_labels = None
depends_on = None

# Références de types ENUM existants/à créer
COMMENT_STATUS = ENUM(
    "visible", "modere", "supprime",
    name="statut_comment_enum",
    create_type=False,  # très important: ne pas créer automatiquement
)
REACTION_TYPE = ENUM(
    "like", "dislike", "love", "laugh", "surprised",
    name="type_reaction_enum",
    create_type=False,  # idem
)

def upgrade() -> None:
    # 1) Créer les types s'ils n'existent pas (idempotent)
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statut_comment_enum') THEN
            CREATE TYPE statut_comment_enum AS ENUM ('visible','modere','supprime');
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_reaction_enum') THEN
            CREATE TYPE type_reaction_enum AS ENUM ('like','dislike','love','laugh','surprised');
        END IF;
    END$$;
    """)

    # 2) Tables
    op.create_table(
        "commentaires",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("pronostic_id", sa.Integer(), sa.ForeignKey("pronostics_utilisateurs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("commentaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("contenu", sa.Text(), nullable=False),
        sa.Column("likes", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("signalements", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("statut", COMMENT_STATUS, server_default=sa.text("'visible'"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Index("ix_commentaires_match_id_created_at", "match_id", "created_at"),
        sa.Index("ix_commentaires_user_id_created_at", "user_id", "created_at"),
    )

    op.create_table(
        "reactions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("commentaire_id", sa.Integer(), sa.ForeignKey("commentaires.id", ondelete="CASCADE"), nullable=True),
        sa.Column("pronostic_id", sa.Integer(), sa.ForeignKey("pronostics_utilisateurs.id", ondelete="CASCADE"), nullable=True),
        sa.Column("type", REACTION_TYPE, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "commentaire_id", name="uq_react_user_comment"),
        sa.UniqueConstraint("user_id", "pronostic_id", name="uq_react_user_pronostic"),
    )

    op.create_table(
        "suivis_utilisateurs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("follower_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("following_id", sa.Integer(), sa.ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("follower_id", "following_id", name="uq_follow_pair"),
    )


def downgrade() -> None:
    # On drop dans l'ordre inverse
    op.drop_table("suivis_utilisateurs")
    op.drop_table("reactions")
    op.drop_table("commentaires")

    # Supprimer les types seulement s'ils ne sont plus utilisés (sécurisé)
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_reaction_enum') THEN
            -- vérifier qu'aucune colonne n'utilise encore le type
            IF NOT EXISTS (
                SELECT 1
                FROM pg_attribute a
                JOIN pg_type t ON a.atttypid = t.oid
                WHERE t.typname = 'type_reaction_enum' AND a.attisdropped = false
            ) THEN
                DROP TYPE type_reaction_enum;
            END IF;
        END IF;

        IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statut_comment_enum') THEN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_attribute a
                JOIN pg_type t ON a.atttypid = t.oid
                WHERE t.typname = 'statut_comment_enum' AND a.attisdropped = false
            ) THEN
                DROP TYPE statut_comment_enum;
            END IF;
        END IF;
    END$$;
    """)
