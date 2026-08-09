from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.workout import DistanceUnit, WorkoutStatus


class WorkoutBase(BaseModel):
    training_week_id: int
    workout_type_id: int
    scheduled_start: datetime
    title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    planned_duration: int | None = Field(default=None, gt=0)
    planned_distance: float | None = Field(default=None, gt=0)
    unit: DistanceUnit | None = None
    status: WorkoutStatus = WorkoutStatus.PLANNED
    completed_at: datetime | None = None
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(WorkoutBase):
    training_week_id: int | None = None
    workout_type_id: int | None = None
    scheduled_start: datetime | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    status: WorkoutStatus | None = None


class WorkoutResponse(WorkoutBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
