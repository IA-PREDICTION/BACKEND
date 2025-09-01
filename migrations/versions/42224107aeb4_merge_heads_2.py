"""merge heads 2

Revision ID: 42224107aeb4
Revises: 322462e16a28, d19e0ab02e72
Create Date: 2025-09-01 21:44:55.137617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42224107aeb4'
down_revision: Union[str, Sequence[str], None] = ('322462e16a28', 'd19e0ab02e72')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
