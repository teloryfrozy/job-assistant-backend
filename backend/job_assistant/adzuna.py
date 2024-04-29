"""
Handles API calls to Adzuna API

The clarity of the code will be improved later on. For now just write request.
We will figure out how to organize it properly on time.
"""

import datetime
import json
import logging
import numpy as np
from scipy import stats
import requests
from gdrive import GoogleDriveManager
from constants import (
    ADZUNA_API,
    ADZUNA_APP_ID,
    ADZUNA_SECRET_KEY,
    STATS_SALARIES_FILE_ID,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


class Adzuna:

    def __init__(self) -> None:
        pass

    def get_params(self, params: dict) -> dict:
        params.update(
            {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_SECRET_KEY,
                "content-type": "application/json",
            }
        )
        return params

    def set_stats(self, job: str, skills: list):
        """Returns average salary according to skills"""

        def get_avg_salary_country(country: str) -> int:
            """TODO: doc of the function."""

            url = f"{ADZUNA_API}jobs/{country}/jobsworth?"
            params = self.get_params({"title": job, "description": ",".join(skills)})

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                salary: int = data["salary"]
                return salary
            else:
                LOGGER.error(f"{response.reason}, {response.status_code}")
                return None

        # TODO: store other useful stats
        # other stats that I forgot: mean, min, max
        # also do this for the main countries (gb, us)

        # also add a doc somewhere to understand what kurtosis and skew means
        # aka: big value = what, small val = what?
        # add on Notion to create an algorithm (later with ML) to interpret these stats values

        data = {}
        countries: list = ["gb", "us"]
        all_salaries = []
        average = 0
        nb_success = 0
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            if data[date]:
                print("Record already created")
                return
        except KeyError:
            pass

        data[date] = {}

        for country in countries:
            result = get_avg_salary_country(country)
            if result:
                nb_success += 1
                average += result
                all_salaries.append(result)
                data[date][country] = result

        data[date]["std_dev"] = int(np.std(all_salaries))
        data[date]["kurtosis"] = float(stats.kurtosis(all_salaries))
        data[date]["skewness"] = float(stats.skew(all_salaries))
        average = int(average / nb_success)
        data[date]["avg"] = average

        # new way to save the data with google drive
        gdrive_manager = GoogleDriveManager()
        gdrive_manager.update_json_file(data, STATS_SALARIES_FILE_ID)
        json_data = gdrive_manager.read_json_file(STATS_SALARIES_FILE_ID)
        print(json.dumps(json_data, indent=4))

    @staticmethod
    def get_jobs(country: str, params: dict, nb_pages: int = 20) -> list:
        """Fetches jobs data from the Adzuna API."""

        params = Adzuna().get_params(params)
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


# TODO: create a representative list of skills for typical jobs
# such as developers, software engineer, network administrator, cyber expert, Data Analyst
# Create a schedule task with "pip install django-crontab" => check doc

Adzuna().set_stats(
    "Full Stack Developer", ["Django, React, Spring, PostgreSQL, Python, Javascript"]
)


# IGNORE THIS FOR NOW
"""
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
"""


# for json_data in results:
#     print(json.dumps(json_data, indent=4))


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
