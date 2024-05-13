"""
Handles API calls to Adzuna API

The clarity of the code will be improved later on. For now just write request.
We will figure out how to organize it properly on time.


TODO: check currency (very very likely to be GBP)



        # also add a doc somewhere to understand what kurtosis and skew means
        # aka: big value = what, small val = what?
        # add on Notion to create an algorithm (later with ML) to interpret these stats values
"""

import datetime
import json
import logging
import numpy as np
from scipy import stats
import requests
from .gdrive import GoogleDriveManager
from .constants import (
    ADZUNA_API,
    ADZUNA_APP_ID,
    ADZUNA_SECRET_KEY,
    STATS_SALARIES_FILE_ID,
)

# TODO: if we can get job offers with all extensions
ADZUNA_COUNTRY_EXTENSIONS = [
    "gb",
    "us",
    "at",
    "au",
    "be",
    "br",
    "ca",
    "ch",
    "de",
    "es",
    "fr",
    "in",
    "it",
    "mx",
    "nl",
    "nz",
    "pl",
    "sg",
    "za",
]


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


class Adzuna:
    """
    Class for interacting with the Adzuna API and performing statistical analysis on job salaries.
    """

    def __init__(self) -> None:
        pass

    def get_params(self, params: dict) -> dict:
        """
        Adds Adzuna API credentials to the request parameters.

        Args:
            params (dict): Dictionary of request parameters.

        Returns:
            dict: Updated dictionary with API credentials.
        """
        params.update(
            {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_SECRET_KEY,
                "content-type": "application/json",
            }
        )
        return params

    def set_stats(self, job: str):
        """
        Retrieves job statistics including average salary, standard deviation, kurtosis, and skewness
        based on job title and skills.

        Args:
            job (str): Job title.
            skills (list): List of skills required for the job.
        """

        def get_avg_salary_country(country: str) -> int:
            """
            Retrieves the average salary for a specific country.

            Args:
                country (str): Country code.

            Returns:
                int: Average salary.
            """
            url = f"{ADZUNA_API}jobs/{country}/jobsworth?"
            params = self.get_params({"title": job})

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                salary: int = data["salary"]
                return salary
            else:
                error_msg = f"Failed to retrieve average salary for country {country}. "
                error_msg += (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return None

        gdrive_manager = GoogleDriveManager()
        json_data: dict = gdrive_manager.read_json_file(STATS_SALARIES_FILE_ID)

        data = {}
        countries = ["gb", "us"]
        all_salaries = []
        average = 0
        nb_success = 0
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not json_data.get(date):
            json_data[date] = {}

        for country in countries:
            result = get_avg_salary_country(country)
            if result:
                nb_success += 1
                average += result
                all_salaries.append(result)
                data[country] = result

        data["std_dev"] = int(np.std(all_salaries))
        data["kurtosis"] = float(stats.kurtosis(all_salaries))
        data["skewness"] = float(stats.skew(all_salaries))
        average = int(average / nb_success)
        data["avg"] = average

        json_data[date][job] = data
        print(json_data)
        gdrive_manager.overwrite_json_file(json_data, STATS_SALARIES_FILE_ID)

    @staticmethod
    def get_jobs(country: str, params: dict, nb_pages: int = 20) -> list:
        """
        Fetches job data from the Adzuna API.

        Args:
            country (str): Country code.
            params (dict): Dictionary of request parameters.
            nb_pages (int, optional): Number of pages to fetch. Defaults to 20.

        Returns:
            list: List of job data.
        """
        params = Adzuna().get_params(params)
        data = []

        for i in range(1, nb_pages + 1):
            url = f"{ADZUNA_API}jobs/{country}/search/{i}?"
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data.append(response.json())
            else:
                error_msg = f"Failed to fetch jobs data from URL: {url}. "
                error_msg += (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return data

        return data
