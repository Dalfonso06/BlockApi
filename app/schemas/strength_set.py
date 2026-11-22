from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StrengthSetBase(BaseModel):
    strength_exercise_id: int
    set_number: int = Field(gt=0)
    reps: int | None = Field(default=None, ge=0)
    weight: float | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, gt=0)
    distance_meters: float | None = Field(default=None, gt=0)
    is_warmup: bool = False


class StrengthSetCreate(StrengthSetBase):
    pass


class StrengthSetUpdate(StrengthSetBase):
    strength_exercise_id: int | None = None
    set_number: int | None = Field(default=None, gt=0)
    is_warmup: bool | None = None


class StrengthSetResponse(StrengthSetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
