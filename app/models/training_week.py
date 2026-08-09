from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class TrainingWeek(Base):
    __tablename__ = "training_weeks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    training_block_id: Mapped[int] = mapped_column(
        ForeignKey("training_blocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    week_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    focus: Mapped[str | None] = mapped_column(
        Text,
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
