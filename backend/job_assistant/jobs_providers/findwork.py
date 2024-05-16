"""
FindWork API Interaction Module

This module is designed to interact with the FindWork API to fetch and analyze job salary data.
Documentation: https://findwork.dev/developers/

Important informations:
    - NO SALARY DATA PROVIDED
"""

import requests
from backend.job_assistant.constants import FINDWORK_SECRET_KEY

API_URL = "https://findwork.dev/api/jobs/"


class FindWork:
    def __init__(self) -> None:
        self.headers = {"Authorization": f"Token {FINDWORK_SECRET_KEY}"}

    def set_number_offers(self, position: str):
        """
        Saves the number of ads for a particular job position.
        """

        url = f"{API_URL}?search={position}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            total_result = data["count"]
            print(f"There are {total_result} results for position {position}")


            # IN A FILE ONLY FOR NUMBER OF JOBS RESULTS (STATS_NUMBER_OFFERS_FILE_ID)
            {
                "05/16/2024": {
                    "FindWork": {
                        position: total_result
                    }
                }
            }

            # TODO: save in gdrive
            # TODO: add color logging print

        else:
            print(f"Error: {response.status_code} - {response.reason}")
