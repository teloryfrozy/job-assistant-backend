"""
Handles API calls to Adzuna API

The clarity of the code will be improved later on. For now just write request.
We will figure out how to organize it properly on time.
"""

import json
import logging
from urllib.parse import urlencode
import requests
from constants import ADZUNA_API, ADZUNA_APP_ID, ADZUNA_SECRET_KEY


LOGGER = logging.getLogger(__name__)


class Request:

    @staticmethod
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

    def get_params(params: dict) -> dict:
        params.update(
            {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_SECRET_KEY,
                "content-type": "application/json",
            }
        )
        return params

    @staticmethod
    def get_jobs(country: str, params: dict, nb_pages: int = 20) -> list:
        """Fetches jobs data from the Adzuna API."""

        params = Request.get_params(params)
        data = []

        for i in range(1, nb_pages + 1):
            url = f"{ADZUNA_API}jobs/{country}/search/{i}?"
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data.append(response.json())
            else:
                LOGGER.error(f"{response.reason}, {response.status_code}")
                return data

        return data


results = Request.get_jobs(
    country="gb",
    params={
        "results_per_page": 20,
        "what": "javascript developer",
        "what_exclude": "java",
        "where": "london",
        "sort_by": "salary",
        "salary_min": 30000,
        "full_time": 1,
        "permanent": 1,
    },
    nb_pages=2,
)


# for json_data in results:
#     print(json.dumps(json_data, indent=4))
















print(Request.get_avg_salary("Software Engineer", ["Django"]))


# TODO: Analyse data output and store a json file

# Create a function that requires skills, job title
# it must return the following

# with the nb of ads in a category, the current date
# the avg salary (anual) => run Request.get_avg_salary
# other stats (standard deviation, kurtosis, skewniss, etc)
# also do this for the main countries (fr, gb, us, de)


"""response = Request.get_jobs(
    country="gb",
    params={
        "results_per_page": 20,
        "what": "javascript developer",
        "what_exclude": "java",
        "where": "london",
        "sort_by": "salary",
        "salary_min": 30000,
        "full_time": 1,
        "permanent": 1,
    },
    nb_pages=2,
)

json_data = response.json()


#This code is just to play around and check
for result in json_data["results"]:
    print(result["id"])
    print(result["title"])
    print(result["description"])
    print(f"location: {result['location']['display_name']}")
    print(f"category: {result['category']['label']}")
    print(f"company: {result['company']['display_name']}")
    print(f"URL: {result['redirect_url']}")
    print(f"Poste: {result['created']}")
    print("\n\n")"""
