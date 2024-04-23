"""
Handles API calls to Adzuna API
"""

import json
import logging
from urllib.parse import urlencode
import requests
from constants import ADZUNA_API, ADZUNA_APP_ID, ADZUNA_SECRET_KEY


LOGGER = logging.getLogger(__name__)


"""
http://api.adzuna.com:80/v1/api/jobs/gb/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}&results_per_page=20&what=javascript%20developer&what_exclude=java&where=london&sort_by=salary&salary_min=30000&full_time=1&permanent=1&content-type=application/json
"""


def get_avg_salary(job: str, skills: list) -> int:
    """Returns average salary according to skills"""

    url = f"{ADZUNA_API}jobs/gb/jobsworth?"
    url += urlencode(
        {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_SECRET_KEY,
            "title": job,
            "description": ",".join(skills),
            "content-type": "application/json",
        }
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        salary = data["salary"]
        return salary
    else:
        LOGGER.error(f"{response.reason}, {response.status_code}")
        return None


def get_jobs(query: str) -> requests.Response:
    """Fetches jobs data from the Adzuna API."""

    url = f"{ADZUNA_API}{query}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_SECRET_KEY,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response
    else:
        LOGGER.error(f"{response.reason}, {response.status_code}")
        return None


response = get_jobs("jobs/gb/search/1")
json_data = response.json()


# print(json.dumps(json_data, indent=4))

for result in json_data["results"]:
    print(result["id"])
    print(result["adref"])
    print(result["title"])
    print(result["description"])
    print(f"location: {result['location']['display_name']}")
    print(f"category: {result['category']['label']}")
    print(f"company: {result['company']['display_name']}")
    print(f"URL: {result['redirect_url']}")
    print(f"Poste: {result['created']}")
