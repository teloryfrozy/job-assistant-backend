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


class ReedCoUk:
    """
    Class for interacting with the Reed CO UK API and performing statistical analysis on job salaries.

    # TODO: add def set_number_offers(self, job_title: str) -> None: method
    """

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        self.job_statistics_manager = job_statistics_manager

    def set_salaries_stats(self, job_title: str):
        """
        Retrieves job statistics including average salary, standard deviation, kurtosis, and skewness, min and max
        based on job title.

        Args:
            job_title (str): Job title.

        TODO:
        add pages to get more than 100 results
        save jobs per currency
        """
        params = {
            "fullTime": "true",
            "keywords": job_title,
        }

        response = requests.get(
            API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
        )

        if response.status_code == 200:
            salaries_data = {}
            data = response.json()

            for job in data["results"]:
                currency = job["currency"]
                if currency not in salaries_data:
                    salaries_data[currency] = {
                        "all_salaries": [],
                        "abs_min_salary": 1_000_000,
                        "abs_max_salary": 0,
                    }

                max_salary = job["maximumSalary"]
                min_salary = job["minimumSalary"]
                if max_salary is not None and min_salary is not None:
                    # sometimes salary is the pay per day
                    if max_salary > 10_000 and min_salary > 10_000:
                        all_salaries: list = salaries_data[currency]["all_salaries"]
                        all_salaries.append(max_salary)
                        all_salaries.append(min_salary)

                        if max_salary > salaries_data[currency]["abs_max_salary"]:
                            salaries_data[currency]["abs_max_salary"] = max_salary
                        if min_salary < salaries_data[currency]["abs_min_salary"]:
                            salaries_data[currency]["abs_min_salary"] = min_salary

                        if max_salary and min_salary:
                            all_salaries.extend([max_salary, min_salary])

                        salaries_data[currency]["all_salaries"] = all_salaries

            if salaries_data:
                self.job_statistics_manager.store_salaries_statistics(
                    job_title, salaries_data
                )
            else:
                LOGGER.error("No salary data available for the given job title.")
        else:
            LOGGER.error(
                f"Failed to retrieve data: {response.status_code} - {response.reason}"
            )

    def get_jobs(self, params: dict) -> dict[str, list] | str:
        """
        TODO: clean doc as a senior backend python developer
        """
        # TODO: add a streaming with a websocket to see a progress bar in FE
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
                    print(result)
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
