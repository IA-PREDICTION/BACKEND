"""widen predictions.prediction_finale to varchar(16)

Revision ID: fb76e91a9186
Revises: 3306764be035
Create Date: 2025-09-01 20:29:50.653996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb76e91a9186'
down_revision: Union[str, Sequence[str], None] = '3306764be035'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column(
        "predictions",
        "prediction_finale",
        existing_type=sa.String(length=1),
        type_=sa.String(length=16),
        existing_nullable=True,
    )

def downgrade():
    # attention: risque de troncature si on revient à 1
    op.alter_column(
        "predictions",
        "prediction_finale",
        existing_type=sa.String(length=16),
        type_=sa.String(length=1),
        existing_nullable=True,
    )