from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.workout import DistanceUnit


class TrainingWeekBase(BaseModel):
    training_block_id: int
    week_number: int = Field(gt=0)
    start_date: date
    end_date: date
    name: str | None = None
    focus: str | None = None


class TrainingWeekCreate(TrainingWeekBase):
    pass


class TrainingWeekUpdate(TrainingWeekBase):
    training_block_id: int | None = None
    week_number: int | None = Field(default=None, gt=0)
    start_date: date | None = None
    end_date: date | None = None


class TrainingWeekResponse(TrainingWeekBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class WorkoutTypeBreakdownItem(BaseModel):
    workout_type: str
    duration_sum: int
    distance: float | None
    unit: DistanceUnit | None


class TrainingWeekBreakdownResponse(BaseModel):
    training_week_id: int
    week_number: int
    start_date: date
    end_date: date
    total_planned_duration_minutes: int
    workout_types: list[WorkoutTypeBreakdownItem]
