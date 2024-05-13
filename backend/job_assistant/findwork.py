"""
TODO: one line clean doc about this API


# DOC: https://findwork.dev/developers/

# ONLY FOR JOB SEARCH - NO SALARY PROVIDED => can still be used for stats
"""

import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.job_assistant.constants import FINDWORK_SECRET_KEY

BASE_URL = "https://findwork.dev/api/jobs/"


class FindWork:
    def __init__(self) -> None:
        self.headers = {"Authorization": f"Token {FINDWORK_SECRET_KEY}"}

    def set_total_results(self, position: str):
        """
        Saves the number of ads for a particular job position.
        """

        url = f"{BASE_URL}?search={position}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            total_result = data["count"]
            print(f"There are {total_result} results for position {position}")

            # TODO: save in gdrive
            # TODO: add color logging print

        else:
            print(f"Error: {response.status_code} - {response.reason}")
