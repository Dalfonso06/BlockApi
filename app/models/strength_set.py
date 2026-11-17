from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class StrengthSet(Base):
    __tablename__ = "strength_sets"
    __table_args__ = (
        UniqueConstraint("strength_exercise_id", "set_number", name="uq_strength_set_exercise_set_number"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    strength_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("strength_activity_details.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    set_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    reps: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    # Canonical unit is kilograms, matching the app-wide "store one base
    # unit, let the frontend convert for display" convention already used
    # for distance (meters) elsewhere — not named in the column itself,
    # consistent with e.g. Workout.planned_distance.
    weight: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    distance_meters: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_warmup: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
