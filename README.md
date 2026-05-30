# Weather API ETL Pipeline

An automated ETL pipeline that extracts live weather data from OpenWeatherMap API, transforms and validates it, and loads it into a MySQL database on an hourly schedule.

## Architecture

OpenWeatherMap API → Extract → Transform → Load (MySQL) → Scheduler (Hourly)

## Tech Stack

- Python
- Pandas
- Requests
- SQLAlchemy
- PyMySQL
- MySQL
- python-dotenv
- schedule

## Features

- Live weather data for 5 cities (Chennai, Mumbai, Delhi, Bengaluru, Hyderabad)
- Data transformation (Kelvin → Celsius conversion)
- Data validation (temperature, humidity, wind speed checks)
- Duplicate prevention using MySQL constraints
- Automated hourly scheduling
- Secure credential management using `.env`
- Logging for monitoring pipeline execution

## Project Structure

```text
weather-etl-pipeline/
├── etl/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── pipeline.py
├── scheduler.py
├── test_api.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md



## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/vinodinib04/weather-etl-pipeline.git
cd weather-etl-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free API key

Sign up at https://openweathermap.org/api and copy your API key.
It activates within 10-15 minutes of signing up.

### 4. Configure environment variables

Create a `.env` file in the root folder

### 5. Set up MySQL database

Open MySQL Workbench and run:

```sql
CREATE DATABASE weather_db;

USE weather_db;

CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(10),
    temperature_celsius FLOAT,
    feels_like_celsius FLOAT,
    humidity INT,
    wind_speed FLOAT,
    weather_description VARCHAR(200),
    recorded_at DATETIME,
    ingested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_city_time (city, recorded_at)
);
```

### 6. Test API connection

```bash
python test_api.py
```

You should see status code 200 and weather data for Chennai.

### 7. Run the pipeline once

```bash
python pipeline.py
```

### 8. Run with hourly scheduler

```bash
python scheduler.py
```

Pipeline will run immediately once, then every hour automatically.
Press Ctrl+C to stop.

## Sample Output

### Terminal
--- Pipeline started at 2026-05-30 10:31:17 ---
Extracting weather data...
Transforming data...
Loading into MySQL...
Load complete: 5 inserted, 0 duplicates skipped
--- Pipeline completed successfully ---
