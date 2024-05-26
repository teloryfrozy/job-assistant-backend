"""
Reed.co.uk API Interaction Module

This module is designed to interact with the Reed.co.uk API to fetch and analyze job salary data.
Documentation: https://www.reed.co.uk/developers/jobseeker 
"""

import logging
import requests
from job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from job_assistant.constants import REED_CO_UK_SECRET_KEY


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
API_URL = "https://www.reed.co.uk/api/1.0/search"
RESULTS_PER_PAGE = 100
ABS_MIN_SALARY = 1_000_000
ABS_MAX_SALARY = 0
SALARY_PER_YEAR = 10_000


# TODO: add def set_number_offers(self, job_title: str) -> None: method


class ReedCoUk:
    """
    Class for interacting with the Reed CO UK API and performing statistical analysis on job salaries.
    """

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        """
        Initialize the ReedCoUk instance.

        Args:
            job_statistics_manager (JobStatisticsManager): An instance of JobStatisticsManager
                responsible for managing and storing job statistics.
        """
        self.job_statistics_manager = job_statistics_manager

    def set_salaries_stats(self, job_title: str):
        """
        Retrieves job statistics including average salary, standard deviation, kurtosis, skewness, min, and max
        based on job title.

        Args:
            job_title (str): Job title.

        The list of salaries is retrieved across multiple pages if necessary.
        """
        params = {
            "fullTime": "true",
            "keywords": job_title,
        }

        response = requests.get(
            API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
        )

        if response.status_code != 200:
            LOGGER.error(
                f"Failed to retrieve data: {response.status_code} - {response.reason}"
            )
            return

        data = response.json()
        total_results = data["totalResults"]
        pages = (total_results // RESULTS_PER_PAGE) + 1

        salaries_data = {}

        for page in range(1, pages + 1):
            params["page"] = page
            response = requests.get(
                API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
            )

            if response.status_code != 200:
                LOGGER.error(
                    f"Failed to retrieve data on page {page}: {response.status_code} - {response.reason}"
                )
                continue

            data = response.json()
            for job in data["results"]:
                currency = job["currency"]
                if currency not in salaries_data and currency is not None:
                    salaries_data[currency] = {
                        "all_salaries": [],
                        "abs_min_salary": ABS_MIN_SALARY,
                        "abs_max_salary": ABS_MAX_SALARY,
                    }

                max_salary = job["maximumSalary"]
                min_salary = job["minimumSalary"]
                if max_salary is not None and min_salary is not None:
                    # sometimes salary is the pay per day
                    if max_salary > SALARY_PER_YEAR and min_salary > SALARY_PER_YEAR:
                        all_salaries: list = salaries_data[currency]["all_salaries"]
                        all_salaries.append(max_salary)
                        all_salaries.append(min_salary)

                        if max_salary > salaries_data[currency]["abs_max_salary"]:
                            salaries_data[currency]["abs_max_salary"] = max_salary
                        if min_salary < salaries_data[currency]["abs_min_salary"]:
                            salaries_data[currency]["abs_min_salary"] = min_salary

                        salaries_data[currency]["all_salaries"] = all_salaries

        if salaries_data:
            self.job_statistics_manager.store_salaries_statistics(
                job_title, salaries_data
            )
        else:
            LOGGER.error("No salary data available for the given job title.")

    def get_jobs(self, params: dict) -> dict[str, list] | str:
        """
        Fetches job listings based on provided search parameters.

        This method interacts with the Reed API to fetch job listings according to the given parameters.
        It handles pagination and aggregates results from multiple pages if necessary.

        Args:
            params (dict): Dictionary of query parameters to be sent to the API.

        Returns:
            dict[str, list]: A dictionary containing the number of offers and a list of job details.
            str: An error message if the API request fails.
        """
        data = {}

        response = requests.get(
            API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
        )
        if response.status_code != 200:
            # TODO: clean logging
            error_msg = (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)
            return error_msg + "There was an error please display something to the user"

        json_data: dict = response.json()
        number_offers = json_data["totalResults"]
        data["number_offers"] = number_offers
        data["results"] = []

        if number_offers < RESULTS_PER_PAGE:
            json_data: dict = response.json()
            results: dict[dict] = json_data["results"]

            for result in results:
                job_info = {
                    "title": result["jobTitle"],
                    "min_salary": result["minimumSalary"],
                    "max_salary": result["maximumSalary"],
                    "currency": result["currency"],
                    "location": result["locationName"],
                    "company": result["employerName"],
                    "url": result["jobUrl"],
                    "date_posted": result["date"],
                    "expiration_date": result["expirationDate"],
                    "applications": result["applications"],
                }
                data["results"].append(job_info)
        else:
            nb_pages = number_offers // RESULTS_PER_PAGE
            if number_offers % RESULTS_PER_PAGE > 0:
                nb_pages += 1

            for i in range(2, nb_pages + 1):
                response = requests.get(
                    API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
                )

                if response.status_code != 200:
                    # TODO: clean logging
                    error_msg = f"PAGE: {i}, Status code: {response.status_code}, Reason: {response.reason}"
                    LOGGER.error(error_msg)
                    return (
                        error_msg
                        + "There was an error please display something to the user"
                    )

                json_data: dict = response.json()
                results: dict = json_data["results"]

                for result in results:
                    job_info = {
                        "title": result["jobTitle"],
                        "min_salary": result["minimumSalary"],
                        "max_salary": result["maximumSalary"],
                        "currency": result["currency"],
                        "location": result["locationName"],
                        "company": result["employerName"],
                        "url": result["jobUrl"],
                        "date_posted": result["date"],
                        "expiration_date": result["expirationDate"],
                        "applications": result["applications"],
                    }
                    data["results"].append(job_info)

        return data
