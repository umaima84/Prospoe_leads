import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

url = "https://api.prospeo.io/search-suggestions"

headers = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "location_search": "Lahore"
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())