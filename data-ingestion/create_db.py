import sqlite3

sql_statement = """
    CREATE TABLE IF NOT EXISTS forecast (
            time varchar(50) PRIMARY KEY NOT NULL, 
            wave_height varchar(50) NOT NULL,
            wave_direction varchar(50) NOT NULL,
            wave_period varchar(50) NOT NULL,
            wind_speed varchar(50) NOT NULL,
            wind_gust varchar(50) NOT NULL,
            wind_direction varchar(50) NOT NULL,
            cloud_coverage varchar(50),
            precipitation varchar(50) NOT NULL,
            air_temperature varchar(50) NOT NULL
        );
"""


# create a database connection
try:
    with sqlite3.connect('forecast.db') as conn:

        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)