import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}"

response = requests.get(url)
print("Status code:", response.status_code)
print("Response:", response.json())