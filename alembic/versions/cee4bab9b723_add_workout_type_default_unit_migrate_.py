"""add workout_type default_unit, migrate distances to meters

Revision ID: cee4bab9b723
Revises: 39cb0c9caf7c
Create Date: 2026-10-13 09:03:21.688051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cee4bab9b723'
down_revision: Union[str, Sequence[str], None] = '39cb0c9caf7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Conversion factors to/from meters. `unit` on `workouts` is kept (not
# dropped) specifically so this migration stays reversible in both
# directions using real data, not just restoring the empty column.
CONVERSION_TO_METERS = {
    'm': 1.0,
    'km': 1000.0,
    'mi': 1609.344,
    'yd': 0.9144,
}

DEFAULT_UNITS_BY_TYPE_NAME = {
    'run': 'mi',
    'bike': 'mi',
    'swim': 'm',
    'lift': None,
}


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('workout_types', sa.Column('default_unit', sa.String(length=10), nullable=True))

    connection = op.get_bind()

    for name, unit in DEFAULT_UNITS_BY_TYPE_NAME.items():
        connection.execute(
            sa.text("UPDATE workout_types SET default_unit = :unit WHERE LOWER(name) = :name"),
            {'unit': unit, 'name': name},
        )

    # Convert existing planned_distance values in-place from their current
    # unit to meters, now that storage is unit-less at the workout level.
    rows = connection.execute(
        sa.text(
            "SELECT id, planned_distance, unit FROM workouts "
            "WHERE planned_distance IS NOT NULL AND unit IS NOT NULL"
        )
    ).fetchall()

    for row in rows:
        factor = CONVERSION_TO_METERS.get(row.unit)
        if factor is not None:
            connection.execute(
                sa.text("UPDATE workouts SET planned_distance = :value WHERE id = :id"),
                {'value': row.planned_distance * factor, 'id': row.id},
            )


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()

    # Reverse the distance conversion first (meters -> original unit) while
    # `unit` is still readable, then drop default_unit.
    rows = connection.execute(
        sa.text(
            "SELECT id, planned_distance, unit FROM workouts "
            "WHERE planned_distance IS NOT NULL AND unit IS NOT NULL"
        )
    ).fetchall()

    for row in rows:
        factor = CONVERSION_TO_METERS.get(row.unit)
        if factor is not None:
            connection.execute(
                sa.text("UPDATE workouts SET planned_distance = :value WHERE id = :id"),
                {'value': row.planned_distance / factor, 'id': row.id},
            )

    op.drop_column('workout_types', 'default_unit')
