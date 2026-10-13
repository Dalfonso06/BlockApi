from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class UserWorkoutTypeUnitPreference(Base):
    __tablename__ = "user_workout_type_unit_preferences"
    __table_args__ = (
        UniqueConstraint("user_id", "workout_type_id", name="uq_user_workout_type_unit_preference"),
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
        ForeignKey("workout_types.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    unit: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
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
