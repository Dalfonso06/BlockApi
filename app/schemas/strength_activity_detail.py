from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StrengthActivityDetailBase(BaseModel):
    activity_id: int
    exercise_id: int
    sequence: int = Field(gt=0)
    notes: str | None = None


class StrengthActivityDetailCreate(StrengthActivityDetailBase):
    pass


class StrengthActivityDetailUpdate(StrengthActivityDetailBase):
    activity_id: int | None = None
    exercise_id: int | None = None
    sequence: int | None = Field(default=None, gt=0)


class StrengthActivityDetailResponse(StrengthActivityDetailBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
