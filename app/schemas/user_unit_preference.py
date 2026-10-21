from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.workout import DistanceUnit


class UserUnitPreferenceSet(BaseModel):
    unit: DistanceUnit


class UserUnitPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    workout_type_id: int
    unit: DistanceUnit
    created_at: datetime
    updated_at: datetime
