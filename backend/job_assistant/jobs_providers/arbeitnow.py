"""
Limitations:
    - ONLY 1 endpoint
    - NO CUSTOM API CALL POSSIBLE 
    - ONLY JOB OFFERS IN GERMANY in tech industry

Features:
    - Tax calculator to estimate net salary (on their website)
"""

import logging
import requests
from datetime import datetime
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)

API_URL = "https://www.arbeitnow.com/api/job-board-api"

RESULTS_PER_PAGE = 100
PAGES_MAX = 30


class ArbeitNow:
    """
    German Tech Jobs (details in German)

    This class provides methods to fetch job listings from the ArbeitNow API.
    """

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        """
        Initializes the ArbeitNow object with a job statistics manager.

        Args:
            job_statistics_manager (JobStatisticsManager): An instance of JobStatisticsManager.
        """
        self.job_statistics_manager = job_statistics_manager

    def get_jobs(self, visa_sponsorship: bool | None) -> dict[str, list] | str:
        """
        TODO: clean the duplicated code with functions
        ⚠️ I already optimized the dichotomous search and chatGPT does not understand it => Do not touch the LOGIC ⚠️

        Fetch job listings from the ArbeitNow API.

        Args:
            visa_sponsorship (bool): Filter jobs by visa sponsorship availability.

        Returns:
            A dictionary containing job listings and metadata, or an error message.
        """

        data = {}
        data["results"] = []

        params = {}
        if visa_sponsorship:
            params["visa_sponsorship"] = visa_sponsorship

        pages = PAGES_MAX
        params["page"] = pages
        response = requests.get(API_URL, params=params)
        if response.status_code != 200:
            # TODO: clean logging
            error_msg = (
                f"Status code: {response.status_code}, Reason: {response.reason}"
            )
            LOGGER.error(error_msg)
            return error_msg + "There was an error please display something to the user"
        json_data: dict = response.json()
        number_offers = json_data["meta"]["to"]

        # FIND page WITH results
        while number_offers is None:
            pages //= 2
            params["page"] = pages
            response = requests.get(API_URL, params=params)
            if response.status_code != 200:
                # TODO: clean logging
                error_msg = (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return (
                    error_msg
                    + "There was an error please display something to the user"
                )
            json_data: dict = response.json()
            number_offers = json_data["meta"]["to"]

        # FIND page WITHOUT results
        while number_offers is not None:
            pages += 1
            params["page"] = pages
            response = requests.get(API_URL, params=params)
            if response.status_code != 200:
                # TODO: clean logging
                error_msg = (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return (
                    error_msg
                    + "There was an error please display something to the user"
                )
            json_data: dict = response.json()
            number_offers = json_data["meta"]["to"]

        # The last page is the one before
        pages -= 1
        params["page"] = pages
        response = requests.get(API_URL, params=params)
        json_data: dict = response.json()
        number_offers = json_data["meta"]["to"]
        data["number_offers"] = number_offers

        for i in range(pages):
            params["page"] = i
            response = requests.get(API_URL, params=params)

            if response.status_code != 200:
                # TODO: clean logging
                error_msg = (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return (
                    error_msg
                    + "There was an error please display something to the user"
                )

            json_data: dict = response.json()
            results: dict[dict] = json_data["data"]

            for result in results:
                date_posted = datetime.fromtimestamp(result["created_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                job_info = {
                    "title": result["title"],
                    "remote": result["remote"],
                    "categories": result.get("tags"),
                    "location": result["location"],
                    "company": result["company_name"],
                    "url": result["url"],
                    "date_posted": date_posted,
                }
                data["results"].append(job_info)

        return data
