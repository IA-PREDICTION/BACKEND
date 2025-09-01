"""merge heads

Revision ID: 322462e16a28
Revises: 52517b63e6ca, fb76e91a9186
Create Date: 2025-09-01 21:39:06.798875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '322462e16a28'
down_revision: Union[str, Sequence[str], None] = ('52517b63e6ca', 'fb76e91a9186')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
