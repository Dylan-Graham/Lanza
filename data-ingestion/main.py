import requests
from bs4 import BeautifulSoup
import json
import re
import sqlite3
from sqlite3 import Connection

URL = "https://www.windfinder.com/forecast/famara"

def degrees_to_cardinal(degrees):
    if degrees is None:
        return None
    
    degrees = degrees % 360
    
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]
    
    index = int((degrees + 11.25) / 22.5) % 16
    
    return directions[index]

def extract_cardinal_direction(svg_element):
    if not svg_element:
        return None
    
    style = svg_element.get('style', '')
    match = re.search(r'rotate\(([\d.]+)deg\)', style)
    
    if not match:
        return None
    
    degrees = float(match.group(1))
    return degrees_to_cardinal(degrees)

def safe_float(x):
    try:
        return float(x)
    except:
        return None

def scrape():
    res = requests.get(URL, headers={"User-Agent": "Chrome/143.0.0.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    # HTML direct mapping to WF :poop-emoji
    days = soup.find_all(class_="fc-day")[:2]

    if not days:
        raise Exception("No forecast days found (structure changed again)")

    for day in days:
        day_label = day.select_one(".fc-day-headline span")
        day_text = day_label.get_text(strip=True) if day_label else "unknown"

        rows = day.select(".fc-table-horizon")

        for row in rows:
            time_el = row.select_one(".cell-ts")
            time_text = time_el.get_text(strip=True) if time_el else None

            wind_speed = safe_float(
                row.select_one(".cell-ws .unit").text
                if row.select_one(".cell-ws .unit") else None
            )

            wind_gust = safe_float(
                row.select_one(".cell-wg .unit").text
                if row.select_one(".cell-wg .unit") else None
            )

            wind_dir_svg = row.select_one(".cell-wd svg")
            wind_dir = extract_cardinal_direction(wind_dir_svg)

            wave_height = safe_float(
                row.select_one(".cell-wh").text
                if row.select_one(".cell-wh") else None
            )

            wave_period = safe_float(
                row.select_one(".cell-wp").text
                if row.select_one(".cell-wp") else None
            )

            wave_dir_svg = row.select_one(".cell-waves-wrapper .cell-wd svg")
            wave_dir = extract_cardinal_direction(wave_dir_svg)

            cloud_el = row.select_one(".cell-cl svg title")
            cloud_coverage = None
            if cloud_el:
                val = cloud_el.text.replace("%", "")
                cloud_coverage = safe_float(val)

            precip_el = row.select_one(".cell-p")
            precipitation = safe_float(precip_el.text) if precip_el and precip_el.text else 0

            temp = safe_float(
                row.select_one(".cell-at .unit").text
                if row.select_one(".cell-at .unit") else None
            )

            entry = {
                "time": f"{day_text} {time_text}",
                "wave_height": wave_height,
                "wave_direction": wave_dir,
                "wave_period": wave_period,
                "wind_speed": wind_speed,
                "wind_gust": wind_gust,
                "wind_direction": wind_dir,
                "cloud_coverage": cloud_coverage,
                "precipitation": (precipitation / 3.0) if precipitation else 0,
                "air_temperature": temp,
            }

            results.append(entry)

    return results

def db_conn() -> Connection:
    try:
        with sqlite3.connect("forecast.db") as conn:
            print(f"Opened SQLite DB with version {sqlite3.version_info}")
    except sqlite3.OperationalError as e:
        print(f"Failed to connect to DB: ({e})")

    return conn

def db_insert(conn: Connection, forecasts):
    sql = """
        INSERT INTO forecast(time, wave_height, wave_direction, wave_period,
        wind_speed, wind_gust, wind_direction, cloud_coverage, precipitation, air_temperature)
        VALUES(?,?,?,?,?,?,?,?,?,?)
    """
    

    try:
        cur = conn.cursor()
        for forecast in forecasts:
            data = (forecast["time"], forecast["wave_height"], forecast["wave_direction"], forecast["wave_period"], forecast["wind_speed"], forecast["wind_gust"], forecast["wind_direction"], forecast["cloud_coverage"], forecast["precipitation"], forecast["air_temperature"])
            cur.execute(sql, data)
        conn.commit()
        print("data added...")
    except sqlite3.Error as e:
        print(f"Error occurred during db insert: {e}")

    return cur.lastrowid
    

if __name__ == "__main__":
    forecasts = scrape()
    conn = db_conn()
    db_insert(conn=conn, forecasts=forecasts)
    # TODO: Logging
