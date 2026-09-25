import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

url = "https://api.prospeo.io/bulk-enrich-person"

headers = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "only_verified_email": True,
    "enrich_mobile": False,
    "data": [
        {
            "identifier": "1",
            "person_id": "aaaa00c7bbd8a647c80e6e04"

        }
    ]
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print("STATUS:", response.status_code)
print("BODY:", response.json())

print("\nHEADERS:")
for key, value in response.headers.items():
    if "rate" in key.lower() or "limit" in key.lower() or "reset" in key.lower():
        print(key, ":", value)


import json

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)

result = response.json()

with open("bulk_enrich_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("Saved to bulk_enrich_output.json")