import pandas as pd
from datetime import datetime
import logging


def kelvin_to_celsius(kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return round(kelvin - 273.15, 2)


def validate_record(record):
    """Validate a transformed record. Returns (is_valid, reason)."""
    if record["temperature_celsius"] < -50 or record["temperature_celsius"] > 60:
        return False, f"Temperature out of range: {record['temperature_celsius']}"
    if record["humidity"] < 0 or record["humidity"] > 100:
        return False, f"Humidity out of range: {record['humidity']}"
    if record["wind_speed"] < 0:
        return False, f"Negative wind speed: {record['wind_speed']}"
    return True, "OK"


def transform(raw_data_list):
    """Transform raw API response list into a clean Pandas DataFrame."""
    records = []

    for raw in raw_data_list:
        try:
            record = {
                "city": raw["name"],
                "country": raw["sys"]["country"],
                "temperature_celsius": kelvin_to_celsius(raw["main"]["temp"]),
                "feels_like_celsius": kelvin_to_celsius(raw["main"]["feels_like"]),
                "humidity": raw["main"]["humidity"],
                "wind_speed": raw["wind"]["speed"],
                "weather_description": raw["weather"][0]["description"],
                "recorded_at": datetime.utcfromtimestamp(raw["dt"])
            }

            is_valid, reason = validate_record(record)
            if is_valid:
                records.append(record)
                logging.info(f"Transformed: {record['city']} - {record['temperature_celsius']}°C")
            else:
                logging.warning(f"Validation failed for {record['city']}: {reason}")

        except KeyError as e:
            logging.error(f"Missing key in raw data: {e}")
        except Exception as e:
            logging.error(f"Transform error: {e}")

    df = pd.DataFrame(records)
    logging.info(f"Transformation complete: {len(df)} valid records")
    return df