from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnduranceActivityDetailSet(BaseModel):
    distance_meters: float | None = None
    elevation_gain_meters: float | None = None
    average_heart_rate: int | None = None
    max_heart_rate: int | None = None
    average_power: int | None = None
    max_power: int | None = None
    average_cadence: float | None = None


class EnduranceActivityDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity_id: int
    distance_meters: float | None
    elevation_gain_meters: float | None
    average_heart_rate: int | None
    max_heart_rate: int | None
    average_power: int | None
    max_power: int | None
    average_cadence: float | None
    created_at: datetime
    updated_at: datetime
