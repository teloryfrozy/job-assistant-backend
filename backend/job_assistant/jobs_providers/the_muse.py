"""
The Muse API Interaction Module

This module is designed to interact with the The Muse API to fetch and analyze job salary data.
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
LOGGER = logging.getLogger(__name__)
THE_MUSE_LEVELS = {
    "Intern": "internship",
    "Junior": "entry",
    "Senior": "senior",
}


class TheMuse:

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        self.job_statistics_manager = job_statistics_manager

    def set_number_offers(self, job_title: str, experience: str) -> None:

        level = THE_MUSE_LEVELS[experience]

        url = f"https://www.themuse.com/api/search-renderer/jobs?ctsEnabled=true&query={job_title}&level={level}&category=software_engineering,computer_it&posted_date_range=last_30d"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            number_offers = data["count"]
            self.job_statistics_manager.store_number_offers(job_title, number_offers)
        else:
            # TODO: LOGGER.ERROR
            print(f"Error: {response.status_code} - {response.reason}")
