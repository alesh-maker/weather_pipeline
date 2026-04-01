# Weather Data Pipeline

## Overview
An end-to-end ETL pipeline that extracts live weather data from the OpenWeatherMap API, loads it into a PostgreSQL database, and transforms it into clean, analysis-ready tables using dbt. The entire pipeline runs inside Docker containers for portability and consistency across environments.

## Architecture
```
OpenWeatherMap API

↓

Python (extract & load)

↓

PostgreSQL (raw storage)

↓

dbt (transform)

↓

Analysis-ready tables
```

## Tech Stack
| Tool | Purpose |
|---|---|
| Python | Extracts data from the API and loads  it   into PostgreSQL. |
| PostgreSQL | Stores raw and transformed weather data. |
| dbt | Transforms raw data into clean, analysis-ready models. |
| Docker | Containerises PostgreSQL for a consistent local environment. |

## Project Structure
```
weather_pipeline/
├── ingestion_folder/
│   └── extract_load_v2.py       # Python ETL script
├── weather_pipeline/          # dbt project
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_weather.sql    # Cleans raw data
│   │   └── marts/
│   │       └── weather_summary.sql # Aggregates insights
│   └── dbt_project.yml
├── .env                       # Credentials (not committed to GitHub)
├── docker-compose.yml         # PostgreSQL container setup
└── requirements.txt           # Python dependencies
```

## dbt Models
### Staging — stg_weather.sql
Selects and standardises all columns from the raw raw_weather table. Acts as a single source of truth for all downstream models.

### Marts — weather_summary.sql
Aggregates the cleaned data by city and country, producing:
- Average, maximum, and minimum temperature
- Average humidity
- Average wind speed
- Total number of readings

## How to Run

### Prerequisites
- Python 3.11+ 
- Docker Desktop
- dbt-postgres

### 1. Clone the repository
```
git clone https://github.com/alesh-maker/weather_pipeline.git
```
cd weather_pipeline

### 2. Create your .env file
```
API_KEY=your_openweathermap_api_key
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=weather_pipeline
DB_USER=admin
DB_PASSWORD=password
```

### 3. Start PostgreSQL with Docker
docker-compose up -d

### 4. Install Python dependencies
pip install -r requirements.txt

### 5. Run the ETL script
python ingestion_folder/extract_load.py

### 6. Run dbt transformations
cd weather_pipeline
dbt run

## Sample Output
After running the pipeline, the weather_summary table produces:
| city | country | avg_temp_c | max_temp_c | min_temp_c | avg_humidity_pct | avg_wind_speed_ms | total_readings |
|---|---|---|---|---|---|---|---|
| Lagos	| NG |	33.40	| 33.85	| 32.05	| 51.25	| 3.39	| 4 |
| London | GB | 15.16	| 15.59	| 14.75	| 66.00	| 2.36	| 4 |
| New York | US	| 13.97	| 17.15	| 4.58	| 73.75	| 6.82	| 4 |
| Tokyo	|JP	|16.83	|18.42	|12.25	|82.00	|3.74	|4|
|Sydney	|AU	|19.45	|20.25	|19.07	|85.25	|2.09	|4|

## What I Learned
- How to connect to and extract data from a REST API using Python;
- How to load structured data into a PostgreSQL database using psycopg2;
- How to transform raw data into clean, analysis-ready models using dbt;
- How to containerise a database using Docker and Docker Compose;
- How to secure credentials using environment variables and a .env file;
- How to structure a data engineering project following industry best practices.

## Next Steps
- Add Apache Airflow to schedule and automate the pipeline;
- Add a second data source and join both in dbt;
- Deploy the pipeline to Azure cloud infrastructure.

## Author

Built by Ola as part of a Generalist Data Engineer portfolio project.