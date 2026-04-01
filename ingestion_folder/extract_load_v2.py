import requests
import psycopg2
from datetime import datetime

from pathlib import Path
from dotenv import load_dotenv
import os
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

#--- Config ---
API_KEY=os.getenv("API_KEY")
CITIES=["London","New York","Lagos","Tokyo","Sydney"]
BASE_URL="http://api.openweathermap.org/data/2.5/weather"

# --- DB Connection ---
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# --- Create Table ---
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_weather(
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                country VARCHAR(10),
                temperature_c FLOAT,
                feels_like_c FLOAT,
                humidity_pct INT,
                weather_description VARCHAR(200),
                wind_speed_ms FLOAT,
                recorded_at TIMESTAMP,
                ingested_at TIMESTAMP DEFAULT NOW()
            );    
        """)
        conn.commit()

#--- Fetch Weather ---
def fetch_weather(city):
    response = requests.get(BASE_URL, params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    })
    response.raise_for_status()
    return response.json()

#--- Insert Weather ---
def insert_weather(conn, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO raw_weather(
                city,
                country,
                temperature_c,
                feels_like_c,
                humidity_pct,
                weather_description,
                wind_speed_ms,
                recorded_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,(
            data["name"],
            data["sys"]["country"],
            data["main"]["temp"],
            data["main"]["feels_like"],
            data["main"]["humidity"],
            data["weather"][0]["description"],
            data["wind"]["speed"],
            datetime.utcfromtimestamp(data["dt"])
        )
        )
        conn.commit()

# --- Main ---
def main():
    conn = get_connection()
    create_table(conn)
    for city in CITIES:
        try:
            data = fetch_weather(city)
            insert_weather(conn, data)
            print(f"✅Inserted weather for {city}")
        except Exception as e:
            print(f"❌Failed for {city}: {e}")
    conn.close()
if __name__ == "__main__":
    main()