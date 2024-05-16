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
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager


######################## LOGGING CONFIGURATION ########################
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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

        url = f"https://www.themuse.com/api/search-renderer/jobs?ctsEnabled=true&query={job_title}&level={level}&category=software_engineering,computer_it&posted_date_range=last_30d"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            number_offers = data["count"]
            self.job_statistics_manager.store_number_offers(job_title, number_offers)
        else:
            LOGGER.error(
                f"Failed to fetch data from The Muse API: {response.status_code} - {response.reason}"
            )
