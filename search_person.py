import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

url = "https://api.prospeo.io/search-person"

headers = {
    "Content-Type": "application/json",
    "X-KEY": API_KEY
}

data = {
    "page": 1,
    "filters": {
        "person_job_title": {
            "include": ["software engineer"],
            "match_mode": "CONTAINS"
        },
        "person_location_search": {
            "include": ["Lahore, Pakistan"]
        }
    }
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

results = response.json()["results"]

for person in results:
    p = person["person"]

    print(
        p["person_id"],
        "|",
        p["full_name"],
        "|",
        p["current_job_title"],
        "|",
        p["location"]["city"]
    )