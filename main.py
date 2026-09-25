import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

url = "https://api.prospeo.io/enrich-person"

headers = {
    "Content-Type": "application/json",
    "X-KEY": API_KEY
}

data = {
    "only_verified_email": True,
    "enrich_mobile": False,
    "data": {
        "person_id": "aaaacd817619fba3d254cd64"
    }
}

response = requests.post(
    url,
    json=data,
    headers=headers
)

print(response.status_code)
print(response.json())