"""
Adzuna API Interaction Module

This module is designed to interact with the Adzuna API to fetch and analyze job salary data.
Documentation: https://developer.adzuna.com/overview
"""

import json
import logging
import time
import requests
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from backend.job_assistant.constants import (
    ADZUNA_API,
    ADZUNA_APP_ID,
    ADZUNA_SECRET_KEY,
)

RESULTS_PER_PAGE = 50
# TODO: check if we can get job offers with all extensions
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

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        self.job_statistics_manager = job_statistics_manager

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

    def set_salaries_stats(self, job: str):
        """
        TODO: Add currency on gdrive: GBP

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

        data = {}
        countries = ["gb", "us"]
        all_salaries = []
        average = 0
        nb_success = 0

        for country in countries:
            result = get_avg_salary_country(country)
            if result:
                nb_success += 1
                average += result
                all_salaries.append(result)
                data[country] = result

        if all_salaries:
            self.job_statistics_manager.store_salaries_statistics(job, all_salaries)

    def set_number_offers(
        self,
        country: str,
        params: dict,
    ):
        """
        Fetches and stores the number of job offers available for a specified country from the Adzuna API.

        Parameters:
            - country (str): The country for which job offers are being queried.
            - params (dict): A dictionary of parameters to modify the API request.
        """
        params = self.get_params(params)
        url = f"{ADZUNA_API}jobs/{country}/search/1"
        response = requests.get(url, params=params)

        if response.status_code == 200:
            number_offers = response.json()["count"]
            self.job_statistics_manager.store_number_offers(
                params["title_only"], number_offers
            )
        else:
            error_msg = f"Failed to fetch jobs data from URL: {url}. "
            error_msg += (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)

    def get_jobs(self, country: str, params: dict) -> list:
        """
        Fetches job data from the Adzuna API.

        Args:
            country (str): Country code.
            params (dict): Dictionary of request parameters.
            nb_pages (int, optional): Number of pages to fetch. Defaults to 20.

        Returns:
            list: List of job data.
        """
        params = self.get_params(params)
        params["results_per_page"] = RESULTS_PER_PAGE

        data = {}
        data["results"] = []

        url = f"{ADZUNA_API}jobs/{country}/search/{1}?"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            # TODO: clean logging
            error_msg = (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)
            return error_msg + "There was an error please display something to the user"

        json_data: dict = response.json()
        number_offers = json_data["count"]
        data["number_offers"] = number_offers
        data["results"] = []

        if number_offers < 100:
            json_data: dict = response.json()
            results: dict = json_data["results"]

            # TODO: add a streaming to see a progress bar in FE
            for result in results:
                job_info = {
                    "title": result["title"],
                    "min_salary": result.get("salary_min"),
                    "max_salary": result.get("salary_max"),
                    "location": result["location"]["display_name"],
                    "category": result["category"]["label"],
                    "company": result["company"]["display_name"],
                    "url": result["redirect_url"],
                    "date_posted": result["created"],
                }
                data["results"].append(job_info)
        else:
            nb_pages = number_offers // RESULTS_PER_PAGE
            if number_offers % RESULTS_PER_PAGE > 0:
                nb_pages += 1

            for i in range(2, nb_pages + 1):
                url = f"{ADZUNA_API}jobs/{country}/search/{i}?"
                response = requests.get(url, params=params)

                if response.status_code != 200:
                    # TODO: clean logging
                    error_msg = f"PAGE: {i}, Status code: {response.status_code}, Reason: {response.reason}"
                    LOGGER.error(error_msg)
                    return (
                        error_msg
                        + "There was an error please display something to the user"
                    )

                json_data: dict = response.json()
                results: dict[dict] = json_data["results"]

                # TODO: add a streaming to see a progress bar in FE
                for result in results:
                    job_info = {
                        "title": result["title"],
                        "min_salary": result.get("salary_min"),
                        "max_salary": result.get("salary_max"),
                        "location": result["location"]["display_name"],
                        "category": result["category"]["label"],
                        "company": result["company"].get("display_name"),
                        "url": result["redirect_url"],
                        "date_posted": result["created"],
                    }
                    data["results"].append(job_info)

        return data
