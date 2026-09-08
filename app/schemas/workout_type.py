from pydantic import BaseModel, ConfigDict, Field


class WorkoutTypeBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class WorkoutTypeCreate(WorkoutTypeBase):
    pass


class WorkoutTypeUpdate(WorkoutTypeBase):
    name: str | None = Field(default=None, min_length=1, max_length=50)


class WorkoutTypeResponse(WorkoutTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
