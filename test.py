import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "X-KEY": API_KEY
}

SEARCH_URL = "https://api.prospeo.io/search-person"
ENRICH_URL = "https://api.prospeo.io/bulk-enrich-person"


# =========================================================
# 1. SEARCH PERSON
# =========================================================

search_data = {
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

print("Searching persons...")

search_response = requests.post(
    SEARCH_URL,
    headers=HEADERS,
    json=search_data
)

print("SEARCH STATUS:", search_response.status_code)

if search_response.status_code != 200:
    print("SEARCH ERROR:")
    print(search_response.text)
    exit()


search_result = search_response.json()

results = search_result.get("results", [])

print("Found IDs:", len(results))


# =========================================================
# 2. SHOW SEARCH RESULTS
# =========================================================

person_ids = []

print("\nSEARCH RESULTS:")
print("-" * 80)

for person in results:

    p = person.get("person", {})

    person_id = p.get("person_id")

    if person_id:
        person_ids.append(person_id)

    print(
        person_id,
        "|",
        p.get("full_name"),
        "|",
        p.get("current_job_title"),
        "|",
        p.get("location", {}).get("city")
    )


# =========================================================
# 3. ENRICH EACH PERSON ONE BY ONE
# =========================================================

enriched_people = []

print("\nStarting enrichment...")
print("5 seconds delay between each person.\n")


for index, person_id in enumerate(person_ids, start=1):

    print(
        f"[{index}/{len(person_ids)}] "
        f"Enriching person: {person_id}"
    )

    enrich_data = {
        "only_verified_email": True,
        "enrich_mobile": False,
        "data": [
            {
                "identifier": str(index),
                "person_id": person_id
            }
        ]
    }

    enrich_response = requests.post(
        ENRICH_URL,
        headers=HEADERS,
        json=enrich_data
    )

    print("STATUS:", enrich_response.status_code)

    if enrich_response.status_code == 200:

        enrich_result = enrich_response.json()

        matched = enrich_result.get("matched", [])

        if matched:

            person_data = matched[0].get("person", {})

            location = person_data.get("location", {})

            output_person = {
                "full_name": person_data.get("full_name"),
                "linkedin_url": person_data.get("linkedin_url"),
                "location": {
                    "state": location.get("state"),
                    "city": location.get("city"),
                    "country": location.get("country")
                },
                "current_job_title": person_data.get(
                    "current_job_title"
                ),
                "email": person_data.get("email")
            }

            enriched_people.append(output_person)

            print(
                "SUCCESS:",
                output_person["full_name"],
                "|",
                output_person["email"]
            )

        else:

            print(
                "NOT MATCHED:",
                person_id
            )

    else:

        print(
            "ENRICH ERROR:",
            enrich_response.text
        )


    # =====================================================
    # WAIT 5 SECONDS BEFORE NEXT ENRICH REQUEST
    # =====================================================

    if index < len(person_ids):
        print("Waiting 5 seconds...\n")
        time.sleep(5)


# =========================================================
# 4. SAVE FINAL OUTPUT
# =========================================================

with open(
    "prospeo_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        enriched_people,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n" + "=" * 80)
print("DONE")
print("=" * 80)

print("Search results:", len(person_ids))
print("Successfully enriched:", len(enriched_people))
print("Output file: prospeo_output.json")