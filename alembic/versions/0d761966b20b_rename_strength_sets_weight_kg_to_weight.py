"""rename strength_sets.weight_kg to weight

Revision ID: 0d761966b20b
Revises: 5268e9b42de3
Create Date: 2026-11-17 18:18:48.357848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d761966b20b'
down_revision: Union[str, Sequence[str], None] = '5268e9b42de3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('strength_sets', 'weight_kg', new_column_name='weight')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('strength_sets', 'weight', new_column_name='weight_kg')
