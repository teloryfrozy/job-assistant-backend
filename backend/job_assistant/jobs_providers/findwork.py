"""
FindWork API Interaction Module

This module is designed to interact with the FindWork API to fetch and analyze job salary data.
Documentation: https://findwork.dev/developers/

Important information:
    - NO SALARY DATA PROVIDED
"""

import logging
import requests
from job_assistant.constants import FINDWORK_SECRET_KEY
from job_assistant.jobs_providers.job_statistics import JobStatisticsManager

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
API_URL = "https://findwork.dev/api/jobs/"
RESULTS_PER_PAGE = 100


class FindWork:
    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        """
        Initializes the FindWork class with necessary headers and a job statistics manager.

        Args:
        job_statistics_manager (JobStatisticsManager): An instance of JobStatisticsManager to manage job data.
        """
        self.headers = {"Authorization": f"Token {FINDWORK_SECRET_KEY}"}
        self.job_statistics_manager = job_statistics_manager

    def set_number_offers(self, job_title: str) -> None:
        """
        Fetches and saves the number of job offers available for a given job title from the FindWork API.

        Args:
        job_title (str): The title of the job to search for.
        """
        job_title_search = job_title.replace(" ", "+")
        url = f"{API_URL}?search={job_title_search}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            number_offers = data["count"]
            self.job_statistics_manager.store_number_offers(job_title, number_offers)
        else:
            # TODO: LOGGER.ERROR
            print(f"Error: {response.status_code} - {response.reason}")

    def get_jobs(self, params: dict) -> dict[str, list] | str:
        """            
        TODO: clean logging with a function (see arbeitnow.py)

        Fetches job data from the Adzuna API.

        Args:
            country (str): Country code.
            params (dict): Dictionary of request parameters.
            nb_pages (int, optional): Number of pages to fetch. Defaults to 20.

        Returns:
            list: List of job data.
        """        
        data = {}
        params["page"] = 1

        response = requests.get(API_URL, headers=self.headers, params=params)
        if response.status_code != 200:
            error_msg = (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)
            return error_msg 

        json_data: dict = response.json()
        number_offers = json_data["count"]
        data["number_offers"] = number_offers
        data["results"] = []

        if number_offers < RESULTS_PER_PAGE:
            json_data: dict = response.json()
            results: dict = json_data["results"]

            for result in results:
                job_info = {
                    "title": result["role"],
                    "location": result["location"],
                    "keywords": result["keywords"],
                    "company": result["company_name"],
                    "url": result["url"],
                    "date_posted": result["date_posted"],
                }
                data["results"].append(job_info)
        else:
            nb_pages = number_offers // RESULTS_PER_PAGE
            if number_offers % RESULTS_PER_PAGE > 0:
                nb_pages += 1

            for i in range(2, nb_pages + 1):
                response = requests.get(API_URL, headers=self.headers, params=params)

                if response.status_code != 200:
                    error_msg = f"PAGE: {i}, Status code: {response.status_code}, Reason: {response.reason}"
                    LOGGER.error(error_msg)
                    return (
                        error_msg
                        
                    )

                json_data: dict = response.json()
                results: dict = json_data["results"]

                for result in results:
                    job_info = {
                        "title": result["role"],
                        "location": result["location"],
                        "keywords": result["keywords"],
                        "company": result["company_name"],
                        "url": result["url"],
                        "date_posted": result["date_posted"],
                    }
                    data["results"].append(job_info)

        return data
