"""sports lot B (odds/stats/h2h/players/injuries)

Revision ID: c3d019f7b973
Revises: 5df273e0b898
Create Date: 2025-08-30 02:10:36.946047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c3d019f7b973'
down_revision: Union[str, Sequence[str], None] = '5df273e0b898'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def _has_table(insp, name: str) -> bool:
    return name in insp.get_table_names()

def _has_index(insp, table: str, index_name: str) -> bool:
    try:
        return any(ix.get("name") == index_name for ix in insp.get_indexes(table))
    except Exception:
        return False

def upgrade():
    bind = op.get_bind()
    insp = inspect(bind)

    # ========== JOUEURS ==========
    if not _has_table(insp, "joueurs"):
        op.create_table(
            "joueurs",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("nom", sa.String(100), nullable=False),
            sa.Column("prenom", sa.String(100)),
            sa.Column("equipe_id", sa.Integer(), sa.ForeignKey("equipes.id", ondelete="SET NULL")),
            sa.Column("position", sa.String(50)),
            sa.Column("numero", sa.Integer()),
            sa.Column("date_naissance", sa.Date()),
            sa.Column("nationalite", sa.String(50)),
            sa.Column("valeur_marchande", sa.Numeric(12, 2)),
            sa.Column("api_id", sa.String(50)),
            sa.Column("actif", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        )

    # ========== BLESSURES / SUSPENSIONS ==========
    if not _has_table(insp, "blessures_suspensions"):
        type_enum = sa.Enum("blessure", "suspension", "autre", name="type_blessure_enum", create_type=False)
        gravite_enum = sa.Enum("legere", "moyenne", "grave", name="gravite_blessure_enum", create_type=False)
        try:
            type_enum.create(bind, checkfirst=True)
            gravite_enum.create(bind, checkfirst=True)
        except Exception:
            pass

        op.create_table(
            "blessures_suspensions",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("joueur_id", sa.Integer(), sa.ForeignKey("joueurs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("equipe_id", sa.Integer(), sa.ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False),
            sa.Column("type", type_enum, nullable=False),
            sa.Column("gravite", gravite_enum),
            sa.Column("date_debut", sa.Date(), nullable=False),
            sa.Column("date_fin_prevue", sa.Date()),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="SET NULL")),
            sa.Column("description", sa.Text()),
            sa.Column("source", sa.String(100)),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    # ========== COTES BOOKMAKERS ==========
    if not _has_table(insp, "cotes_bookmakers"):
        op.create_table(
            "cotes_bookmakers",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("bookmaker", sa.String(50), nullable=False),
            sa.Column("cote_dom", sa.Numeric(5, 2), nullable=False),
            sa.Column("cote_nul", sa.Numeric(5, 2)),
            sa.Column("cote_ext", sa.Numeric(5, 2), nullable=False),
            sa.Column("cote_over_2_5", sa.Numeric(5, 2)),
            sa.Column("cote_under_2_5", sa.Numeric(5, 2)),
            sa.Column("cote_btts_oui", sa.Numeric(5, 2)),
            sa.Column("cote_btts_non", sa.Numeric(5, 2)),
            sa.Column("date_maj", sa.TIMESTAMP(), nullable=False),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )
        # index composite
        if not _has_index(insp, "cotes_bookmakers", "ix_cotes_match_bkm_date"):
            op.create_index(
                "ix_cotes_match_bkm_date",
                "cotes_bookmakers",
                ["match_id", "bookmaker", "date_maj"],
                unique=False,
            )

    # ========== STATISTIQUES MATCHS ==========
    if not _has_table(insp, "statistiques_matchs"):
        op.create_table(
            "statistiques_matchs",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False, unique=True),
            sa.Column("possession_dom", sa.Numeric(5, 2)),
            sa.Column("possession_ext", sa.Numeric(5, 2)),
            sa.Column("tirs_dom", sa.Integer()),
            sa.Column("tirs_ext", sa.Integer()),
            sa.Column("tirs_cadres_dom", sa.Integer()),
            sa.Column("tirs_cadres_ext", sa.Integer()),
            sa.Column("corners_dom", sa.Integer()),
            sa.Column("corners_ext", sa.Integer()),
            sa.Column("fautes_dom", sa.Integer()),
            sa.Column("fautes_ext", sa.Integer()),
            sa.Column("cartons_jaunes_dom", sa.Integer()),
            sa.Column("cartons_jaunes_ext", sa.Integer()),
            sa.Column("cartons_rouges_dom", sa.Integer()),
            sa.Column("cartons_rouges_ext", sa.Integer()),
            sa.Column("xg_dom", sa.Numeric(5, 2)),
            sa.Column("xg_ext", sa.Numeric(5, 2)),
            sa.Column("passes_reussies_dom", sa.Integer()),
            sa.Column("passes_reussies_ext", sa.Integer()),
            sa.Column("hors_jeux_dom", sa.Integer()),
            sa.Column("hors_jeux_ext", sa.Integer()),
            sa.Column("meta", sa.dialects.postgresql.JSONB(), nullable=True),  # évite le nom réservé "metadata"
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    # ========== HISTORIQUES CONFRONTATIONS ==========
    if not _has_table(insp, "historiques_confrontations"):
        lieu_enum = sa.Enum("domicile_eq1", "domicile_eq2", "neutre", name="lieu_h2h_enum", create_type=False)
        try:
            lieu_enum.create(bind, checkfirst=True)
        except Exception:
            pass

        op.create_table(
            "historiques_confrontations",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("equipe1_id", sa.Integer(), sa.ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False),
            sa.Column("equipe2_id", sa.Integer(), sa.ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False),
            sa.Column("match_id", sa.Integer(), sa.ForeignKey("matchs.id", ondelete="CASCADE"), nullable=False),
            sa.Column("date_match", sa.TIMESTAMP(), nullable=False),
            sa.Column("score_equipe1", sa.Integer()),
            sa.Column("score_equipe2", sa.Integer()),
            sa.Column("lieu", lieu_enum),
            sa.Column("championnat_id", sa.Integer(), sa.ForeignKey("championnats.id", ondelete="SET NULL")),
        )

def downgrade():
    bind = op.get_bind()
    insp = inspect(bind)

    if _has_table(insp, "historiques_confrontations"):
        op.drop_table("historiques_confrontations")
        try:
            sa.Enum(name="lieu_h2h_enum").drop(bind, checkfirst=True)
        except Exception:
            pass

    if _has_table(insp, "statistiques_matchs"):
        op.drop_table("statistiques_matchs")

    if _has_table(insp, "cotes_bookmakers"):
        if _has_index(insp, "cotes_bookmakers", "ix_cotes_match_bkm_date"):
            op.drop_index("ix_cotes_match_bkm_date", table_name="cotes_bookmakers")
        op.drop_table("cotes_bookmakers")

    if _has_table(insp, "blessures_suspensions"):
        op.drop_table("blessures_suspensions")
        try:
            sa.Enum(name="type_blessure_enum").drop(bind, checkfirst=True)
            sa.Enum(name="gravite_blessure_enum").drop(bind, checkfirst=True)
        except Exception:
            pass

    if _has_table(insp, "joueurs"):
        op.drop_table("joueurs")

def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistiques_matchs')
    op.drop_table('historiques_confrontations')
    op.drop_index('ix_cotes_match_book_date', table_name='cotes_bookmakers')
    op.drop_table('cotes_bookmakers')
    op.drop_table('blessures_suspensions')
    op.drop_table('joueurs')
    # ### end Alembic commands ###
