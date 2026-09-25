import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

response = requests.get(
    "https://api.prospeo.io/account-information",
    headers={
        "X-KEY": API_KEY
    }
)

print(response.status_code)
print(response.json())