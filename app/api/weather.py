from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.weather import WeatherResponse
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=WeatherResponse)
def get_current_weather(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    current_user: User = Depends(get_current_user),
):
    return weather_service.get_current_weather(latitude, longitude)
