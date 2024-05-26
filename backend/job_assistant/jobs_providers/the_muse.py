"""
The Muse API Interaction Module

This module is designed to interact with The Muse API to fetch and analyze job data.
Documentation: https://www.themuse.com/developers/api/v2

Important information:
    - PUBLIC API
    - NO SALARY DATA PROVIDED
    - PLENTY OF PARAMETERS
"""

import logging
import requests
from job_assistant.jobs_providers.job_statistics import JobStatisticsManager


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
API_URL = "https://www.themuse.com/api/public/"
RESULTS_PER_PAGE = 20
THE_MUSE_LEVELS = {
    "Intern": "internship",
    "Junior": "entry",
    "Senior": "senior",
}


class TheMuse:
    """
    A class to interact with The Muse API for fetching job data.

    Attributes:
        job_statistics_manager (JobStatisticsManager): A manager to handle job statistics storage.
    """

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        """
        Initializes the TheMuse object with a job statistics manager.

        Args:
            job_statistics_manager (JobStatisticsManager): An instance of JobStatisticsManager.
        """
        self.job_statistics_manager = job_statistics_manager

    def set_number_offers(self, job_title: str, experience: str) -> None:
        """
        Fetches the number of job offers for a given title and experience level from The Muse API and stores it.

        Args:
            job_title (str): The title of the job to search for.
            experience (str): The experience level of the job (Intern, Junior, Senior).
        """
        level = THE_MUSE_LEVELS[experience]

        url = "https://www.themuse.com/api/search-renderer/jobs"

        # TODO: add more categories according to job title
        params = {
            "ctsEnabled": "true",  # essential
            "query": job_title,
            "level": level,
            "category": "software_engineering,computer_it",
            "posted_date_range": "last_30d",  # essential
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            number_offers = data["count"]
            self.job_statistics_manager.store_number_offers(job_title, number_offers)
        else:
            LOGGER.error(
                f"Failed to fetch data from The Muse API: {response.status_code} - {response.reason}"
            )

    def get_jobs(self, params: dict) -> dict[str, list] | str:
        """
        TODO: clean doc as a senior backend python developer
        """
        
        data = {}
        params["page"] = 1
        response = requests.get(f"{API_URL}jobs", params=params)

        if response.status_code != 200:
            # TODO: clean logging
            error_msg = (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)
            return error_msg + "There was an error please display something to the user"

        json_data: dict = response.json()
        number_offers = json_data["total"] if json_data["results"] != [] else 0
        data["number_offers"] = number_offers
        data["results"] = []

        if number_offers < RESULTS_PER_PAGE:
            json_data: dict = response.json()
            results: dict[dict] = json_data["results"]

            for result in results:
                job_info = {
                    "title": result["name"],
                    "categories": result.get("categories"),
                    "location": result["locations"],
                    "company": result["company"]["name"],
                    "url": result["refs"]["landing_page"],
                    "date_posted": result["publication_date"],
                }
                data["results"].append(job_info)
        else:
            nb_pages = json_data["page_count"]

            for i in range(2, nb_pages + 1):
                params["page"] = i
                response = requests.get(f"{API_URL}jobs", params=params)

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

                for result in results:
                    job_info = {
                        "title": result["name"],
                        "categories": result.get("categories"),
                        "location": result["locations"],
                        "company": result["company"]["name"],
                        "url": result["refs"]["landing_page"],
                        "date_posted": result["publication_date"],
                    }
                    data["results"].append(job_info)

        return data
