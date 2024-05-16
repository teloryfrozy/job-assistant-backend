"""
This module computes and stores job salary statistics on Google Drive, tailored for different job APIs.



# TODO
# also add a doc somewhere to understand what kurtosis and skew means
# aka: big value = what, small val = what?
# add on Notion to create an algorithm (later with ML) to interpret these stats values
"""

import datetime
import json
import numpy as np
from scipy import stats
from colorama import Fore, init
import logging
from backend.job_assistant.gdrive import GoogleDriveManager
from backend.job_assistant.constants import STATS_SALARIES_FILE_ID

LOGGER = logging.getLogger(__name__)
init(autoreset=True)


class JobStatisticsManager:
    """
    Manages the computation and storage of job statistics.
    """

    def __init__(self, gdrive_manager: GoogleDriveManager, api_name: str):
        """
        Initializes the JobStatisticsManager with a specific Google Drive manager and API name.

        Args:
            gdrive_manager (GoogleDriveManager): The Google Drive manager to handle file operations.
            api_name (str): The name of the API to manage statistics for.
        """
        self.gdrive_manager = gdrive_manager
        self.api_name = api_name

    def store_salaries_statistics(
        self,
        job_title: str,
        all_salaries: list,
        min_salary: int = None,
        max_salary: int = None,
    ) -> None:
        """
        Computes statistics from salary data and stores them in a structured JSON file on Google Drive.

        Args:
            job_title (str): The title of the job for which statistics are being calculated.
            all_salaries (list): A list of salaries from which to calculate statistics.
            min_salary (int, optional): The minimum salary for the job title. Defaults to None.
            max_salary (int, optional): The maximum salary for the job title. Defaults to None.

        Updates the JSON file on Google Drive with new statistics under the current date and API name.
        """
        json_data = self.gdrive_manager.read_json_file(STATS_SALARIES_FILE_ID)
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if date not in json_data:
            json_data[date] = {}

        if self.api_name not in json_data[date]:
            json_data[date][self.api_name] = {}
        else:
            LOGGER.info(
                f"Salaries stats already saved for API: {self.api_name} on {date}"
            )
            return

        stats_data = {
            "std_dev": int(np.std(all_salaries)),
            "kurtosis": float(stats.kurtosis(all_salaries)),
            "skewness": float(stats.skew(all_salaries)),
            "avg": int(np.mean(all_salaries)),
        }

        if min_salary is not None:
            stats_data["min"] = min_salary
        if max_salary is not None:
            stats_data["max"] = max_salary

        json_data[date][self.api_name][job_title] = stats_data
        self.gdrive_manager.overwrite_json_file(json_data, STATS_SALARIES_FILE_ID)
        LOGGER.info(f"{Fore.GREEN}Statistics stored for {job_title}: {stats_data}")

        print("--------- FILE DATA AFTER UPDATE ------")
        file_data = self.gdrive_manager.read_json_file(STATS_SALARIES_FILE_ID)
        print(json.dumps(file_data[date], indent=4))
