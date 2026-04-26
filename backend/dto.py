from typing import Optional

from pydantic import BaseModel

class Forecast(BaseModel):
    time: str
    wave_height: str
    wave_direction: str
    wave_period: str
    wind_speed: str
    wind_gust: str
    wind_direction: str
    cloud_coverage: Optional[str]
    precipitation: str
    air_temperature: str

class SpotRating(BaseModel):
    spot: str
    rating: float
    reasons: list[str]

class ForecastRating(BaseModel):
    time: str
    spot_ratings: list[SpotRating]