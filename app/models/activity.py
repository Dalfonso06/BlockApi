from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        Index("ix_activities_user_id_started_at", "user_id", "started_at"),
        UniqueConstraint("source_id", "external_id", name="uq_activity_source_external_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    workout_type_id: Mapped[int] = mapped_column(
        ForeignKey("workout_types.id"),
        nullable=False,
        index=True,
    )

    planned_workout_id: Mapped[int | None] = mapped_column(
        ForeignKey("workouts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    elapsed_duration_seconds: Mapped[int] = mapped_column(
        nullable=False,
    )

    moving_duration_seconds: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    # Session-level, not per-exercise: a heart rate monitor tracks the whole
    # activity continuously, so this lives here rather than on any
    # category-specific detail table (e.g. StrengthActivityDetail).
    average_heart_rate: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    max_heart_rate: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
        index=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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
