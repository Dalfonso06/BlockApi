from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SourceBase(BaseModel):
    key: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    is_enabled: bool = True


class SourceCreate(SourceBase):
    pass


class SourceUpdate(SourceBase):
    key: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    is_enabled: bool | None = None


class SourceResponse(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
