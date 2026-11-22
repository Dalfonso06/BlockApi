from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.exercise import ExerciseCategory


class ExerciseBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    category: ExerciseCategory
    description: str | None = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(ExerciseBase):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    category: ExerciseCategory | None = None


class ExerciseResponse(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
