import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CITIES = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad"]
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def extract_weather(city):
    """Fetch raw weather data for a city from OpenWeatherMap API."""
    try:
        params = {"q": city, "appid": API_KEY}
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Extracted data for {city}")
        return data
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error for {city}: {e}")
        return None
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection error for {city}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for {city}: {e}")
        return None


def extract_all():
    """Extract weather data for all configured cities."""
    results = []
    for city in CITIES:
        data = extract_weather(city)
        if data:
            results.append(data)
    logging.info(f"Extraction complete: {len(results)}/{len(CITIES)} cities successful")
    return results