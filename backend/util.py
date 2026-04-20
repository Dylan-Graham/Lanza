import json
from pydantic import BaseModel

from backend.dto import Forecast, SpotRating

class SurfLevelRecommendation(BaseModel):
    beginner: int
    advanced: int
    expert: int

class Spot(BaseModel):
    name: str
    town: str
    location: str
    description: str
    wind_directions: list[str]
    swell_directions: list[str]
    tides: list[str]
    wave_size: list[int]
    wave_types: list[str]
    wave_power: list[str]
    surf_level_recommendation: SurfLevelRecommendation


SIXTEEN_POINT_COMPASS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]


class Score(BaseModel):
    rating: float
    reason: str


def wind_direction_score(wind_direction: str, spot_wind_direction: list[str]) -> Score:
    match = wind_direction in spot_wind_direction
    
    first = spot_wind_direction[0]
    last = spot_wind_direction[-1]
    first_idx = SIXTEEN_POINT_COMPASS.index(first)
    last_idx = SIXTEEN_POINT_COMPASS.index(last)
    std_dev_start = SIXTEEN_POINT_COMPASS[(first_idx-1)%16]
    std_dev_end = SIXTEEN_POINT_COMPASS[(last_idx+1)%16]
    std_dev = [std_dev_start, std_dev_end]
    std_deviation = wind_direction in std_dev

    if match:
        return Score(rating=2, reason="Perfect wind")
    if std_deviation:
        return Score(rating=1.25, reason="Fair wind")
    return Score(rating=0, reason="Poor wind direction")


def wave_direction_score(wave_direction: str, spot_swell_direction: list[str]) -> Score:
    match = wave_direction in spot_swell_direction

    first = spot_swell_direction[0]
    last = spot_swell_direction[-1]
    first_idx = SIXTEEN_POINT_COMPASS.index(first)
    last_idx = SIXTEEN_POINT_COMPASS.index(last)
    std_dev_start = SIXTEEN_POINT_COMPASS[(first_idx-1)%16]
    std_dev_end = SIXTEEN_POINT_COMPASS[(last_idx+1)%16]
    std_dev = [std_dev_start, std_dev_end]
    std_deviation = wave_direction in std_dev

    if match:
        return Score(rating=3, reason="Perfect swell direction")
    if std_deviation:
        return Score(rating=1.5, reason="Fair swell direction")
    return Score(rating=0, reason="Poor swell direction")


def wave_height_score(wave_height: float, spot_wave_size: list[int]) -> Score:
    lo = float(spot_wave_size[0])
    hi = float(spot_wave_size[1])

    if lo < wave_height < hi:
        return Score(rating=2, reason="Perfect wave size")
    if lo - 0.5 <= wave_height <= hi + 0.5:
        return Score(rating=1, reason="Fair wave size")
    return Score(rating=0, reason="Poor wave size")


def wave_period_score(wave_period: int) -> Score:
    if wave_period < 0:
        raise ValueError("Wave period must be positive!")
    if wave_period > 12:
        return Score(rating=1.5, reason="Perfect wave period")
    if 8 <= wave_period <= 12:
        return Score(rating=1, reason="Fair wave period")
    if 6 <= wave_period < 8:
        return Score(rating=0.5, reason="Okay wave period")
    return Score(rating=0, reason="Poor wave period")


def wind_speed_score(wind_speed: int) -> Score:
    if wind_speed < 0:
        raise ValueError("Wind speed must be positive!")
    if wind_speed > 10:
        return Score(rating=0, reason="Wind over 10 knots")
    if 5 <= wind_speed <= 10:
        return Score(rating=0.5, reason="Minimal wind")
    return Score(rating=1, reason="Perfect glassy conditions")


def rate_spot(forecast: Forecast, spot: Spot) -> dict[float, list[str]]:

    wind_dir = wind_direction_score(forecast.wind_direction, spot.wind_directions)
    wave_dir = wave_direction_score(forecast.wave_direction, spot.swell_directions)
    wave_hgt = wave_height_score(float(forecast.wave_height), spot.wave_size)
    wave_prd = wave_period_score(int(forecast.wave_period))
    wind_spd = wind_speed_score(int(forecast.wind_speed))

    rating = (
        wind_dir.rating
        + wave_dir.rating
        + wave_hgt.rating
        + wave_prd.rating
        + wind_spd.rating
    )
    reasons = [
        wind_dir.reason,
        wave_dir.reason,
        wave_hgt.reason,
        wave_prd.reason,
        wind_spd.reason
    ]
    return {
        "rating": rating / 2,
        "reasons": reasons

    } 

forecast = Forecast(
    time="",
    wave_height="0.9",
    wave_direction="WNW",
    wave_period="9",
    wind_speed="13",
    wind_gust="14",
    wind_direction="WSW",
    cloud_coverage=None,
    precipitation="",
    air_temperature="19"
)

def ratings() -> list[SpotRating]:
    ratings: list[SpotRating] = []
    
    # Move to run once at start-up
    spots: list[Spot] = []
    with open("spot-guide.json", "r", encoding="utf8") as jsonfile: 
        data = json.load(jsonfile)
        for d in data:
            spots.append(
            Spot(**d) 
            )

    for spot in spots:
        spot_rating = rate_spot(forecast=forecast, spot=spot)
        ratings.append(
            SpotRating(spot=spot.name, rating=spot_rating["rating"], reasons=spot_rating["reasons"])
        )

    return ratings