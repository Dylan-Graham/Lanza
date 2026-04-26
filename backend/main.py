from fastapi import FastAPI
import sqlite3

from backend.dto import Forecast, ForecastRating
from backend.util import ratings, load_spot_guide

app = FastAPI()

spots = load_spot_guide()

@app.get("/forecasts", response_model=list[Forecast])
async def list_forecasts():
    try:
        with sqlite3.connect("../data-ingestion/forecast.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "select time, wave_height, wave_direction, wave_period, wind_speed, wind_gust, wind_direction, cloud_coverage, precipitation, air_temperature from forecast"
            )
            rows = cur.fetchall()

            # Serialization
            forecasts =[Forecast(**dict(row)) for row in rows]
    except sqlite3.OperationalError as e:
        print(f"Error fetching data: ({e})")

    return forecasts

@app.get("/ratings", response_model=list[ForecastRating])
async def list_ratings():
    try:
        with sqlite3.connect("../data-ingestion/forecast.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # TODO: Only last 24 hours
            cur.execute(
                "select time, wave_height, wave_direction, wave_period, wind_speed, wind_gust, wind_direction, cloud_coverage, precipitation, air_temperature from forecast"
            )
            rows = cur.fetchall()

            forecasts =[Forecast(**dict(row)) for row in rows]
            spot_ratings = ratings(forecasts=forecasts, spots=spots)
    except sqlite3.OperationalError as e:
        print(f"Error fetching data: ({e})")

    return spot_ratings
