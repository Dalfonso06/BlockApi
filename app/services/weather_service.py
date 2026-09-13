import httpx

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.schemas.weather import WMO_CODE_TO_CONDITION, WeatherCondition, WeatherResponse

settings = get_settings()


def _map_weather_code(code: int) -> WeatherCondition:
    return WMO_CODE_TO_CONDITION.get(code, WeatherCondition.CLOUDY)


def get_current_weather(latitude: float, longitude: float) -> WeatherResponse:
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

    return WeatherResponse(
        latitude=latitude,
        longitude=longitude,
        temperature=temperature,
        condition=_map_weather_code(weather_code),
    )
