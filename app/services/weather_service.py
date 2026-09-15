import threading
import time

import httpx

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.schemas.weather import WMO_CODE_TO_CONDITION, WeatherCondition, WeatherResponse

settings = get_settings()

_CACHE_TTL_SECONDS = 600
_CACHE_PRECISION = 2

_cache: dict[tuple[float, float], tuple[float, float, WeatherCondition]] = {}
_cache_lock = threading.Lock()


def _map_weather_code(code: int) -> WeatherCondition:
    return WMO_CODE_TO_CONDITION.get(code, WeatherCondition.CLOUDY)


def _cache_key(latitude: float, longitude: float) -> tuple[float, float]:
    return (round(latitude, _CACHE_PRECISION), round(longitude, _CACHE_PRECISION))


def get_current_weather(latitude: float, longitude: float) -> WeatherResponse:
    key = _cache_key(latitude, longitude)

    with _cache_lock:
        cached = _cache.get(key)
        if cached is not None:
            expires_at, temperature, condition = cached
            if expires_at > time.monotonic():
                return WeatherResponse(
                    latitude=latitude,
                    longitude=longitude,
                    temperature=temperature,
                    condition=condition,
                )

    try:
        response = httpx.get(
            settings.open_meteo_base_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code",
                "temperature_unit": "fahrenheit",
            },
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise ExternalServiceError("Failed to fetch weather data") from exc

    current = response.json().get("current", {})
    temperature = current.get("temperature_2m")
    weather_code = current.get("weather_code")

    if temperature is None or weather_code is None:
        raise ExternalServiceError("Weather provider returned an unexpected response")

    condition = _map_weather_code(weather_code)

    with _cache_lock:
        _cache[key] = (time.monotonic() + _CACHE_TTL_SECONDS, temperature, condition)

    return WeatherResponse(
        latitude=latitude,
        longitude=longitude,
        temperature=temperature,
        condition=condition,
    )
