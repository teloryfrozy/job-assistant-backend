"""
FindWork API Interaction Module

This module is designed to interact with the FindWork API to fetch and analyze job salary data.
Documentation: https://findwork.dev/developers/

Important informations:
    - NO SALARY DATA PROVIDED
"""

import requests
from backend.job_assistant.constants import FINDWORK_SECRET_KEY
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager

API_URL = "https://findwork.dev/api/jobs/"


class FindWork:
    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        self.headers = {"Authorization": f"Token {FINDWORK_SECRET_KEY}"}
        self.job_statistics_manager = job_statistics_manager

    def set_number_offers(self, job_title: str):
        """
        Saves the number of ads for a particular job_title.
        """
        job_title_search = job_title.replace(" ", "+")
        url = f"{API_URL}?search={job_title_search}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            number_offers = data["count"]
            self.job_statistics_manager.store_number_offers(job_title, number_offers)

        else:
            print(f"Error: {response.status_code} - {response.reason}")
