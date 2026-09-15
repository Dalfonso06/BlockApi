import enum

from pydantic import BaseModel


class WeatherCondition(str, enum.Enum):
    CLEAR = "clear"
    PARTLY_CLOUDY = "partly_cloudy"
    CLOUDY = "cloudy"
    FOG = "fog"
    DRIZZLE = "drizzle"
    RAIN = "rain"
    SNOW = "snow"
    THUNDERSTORM = "thunderstorm"


# Maps Open-Meteo's WMO weather codes (https://open-meteo.com/en/docs) down to
# our own small, stable set so the frontend's icon set doesn't depend on
# Open-Meteo's exact numbering.
WMO_CODE_TO_CONDITION: dict[int, WeatherCondition] = {
    0: WeatherCondition.CLEAR,
    1: WeatherCondition.PARTLY_CLOUDY,
    2: WeatherCondition.PARTLY_CLOUDY,
    3: WeatherCondition.CLOUDY,
    45: WeatherCondition.FOG,
    48: WeatherCondition.FOG,
    51: WeatherCondition.DRIZZLE,
    53: WeatherCondition.DRIZZLE,
    55: WeatherCondition.DRIZZLE,
    56: WeatherCondition.DRIZZLE,
    57: WeatherCondition.DRIZZLE,
    61: WeatherCondition.RAIN,
    63: WeatherCondition.RAIN,
    65: WeatherCondition.RAIN,
    66: WeatherCondition.RAIN,
    67: WeatherCondition.RAIN,
    71: WeatherCondition.SNOW,
    73: WeatherCondition.SNOW,
    75: WeatherCondition.SNOW,
    77: WeatherCondition.SNOW,
    80: WeatherCondition.RAIN,
    81: WeatherCondition.RAIN,
    82: WeatherCondition.RAIN,
    85: WeatherCondition.SNOW,
    86: WeatherCondition.SNOW,
    95: WeatherCondition.THUNDERSTORM,
    96: WeatherCondition.THUNDERSTORM,
    99: WeatherCondition.THUNDERSTORM,
}


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    condition: WeatherCondition
