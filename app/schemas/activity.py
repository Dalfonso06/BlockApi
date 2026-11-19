from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ActivityBase(BaseModel):
    workout_type_id: int
    planned_workout_id: int | None = None
    name: str | None = Field(default=None, max_length=150)
    started_at: datetime
    elapsed_duration_seconds: int = Field(gt=0)
    moving_duration_seconds: int | None = Field(default=None, gt=0)
    notes: str | None = None
    source_id: int
    external_id: str | None = Field(default=None, max_length=255)


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    workout_type_id: int | None = None
    started_at: datetime | None = None
    elapsed_duration_seconds: int | None = Field(default=None, gt=0)
    source_id: int | None = None


class ActivityResponse(ActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
