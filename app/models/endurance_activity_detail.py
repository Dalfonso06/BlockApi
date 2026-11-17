from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class EnduranceActivityDetail(Base):
    __tablename__ = "endurance_activity_details"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    distance_meters: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    elevation_gain_meters: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    average_heart_rate: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    max_heart_rate: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    average_power: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    max_power: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    average_cadence: Mapped[float | None] = mapped_column(
        Float,
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
