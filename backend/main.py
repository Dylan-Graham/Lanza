from typing import List

from fastapi import FastAPI
import sqlite3

from backend.dto import Forecast

app = FastAPI()


@app.get("/forecasts", response_model=List[Forecast])
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
