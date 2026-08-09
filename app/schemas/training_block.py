from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.training_block import TrainingBlockStatus


class TrainingBlockBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    start_date: date
    end_date: date
    status: TrainingBlockStatus = TrainingBlockStatus.PLANNED


class TrainingBlockCreate(TrainingBlockBase):
    pass


class TrainingBlockUpdate(TrainingBlockBase):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    start_date: date | None = None
    end_date: date | None = None
    status: TrainingBlockStatus | None = None


class TrainingBlockResponse(TrainingBlockBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
