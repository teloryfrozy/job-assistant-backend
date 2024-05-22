"""
This module computes and stores job salary statistics on Google Drive, tailored for different job APIs.

Statistical Concepts:
    Kurtosis:
        - Measures the "tailedness" of the data distribution.
        - High kurtosis: Sharp peak, heavy tails (more outliers).
        - Low kurtosis: Flatter peak, light tails (fewer outliers).

    Skewness:
        - Measures the asymmetry of the data distribution.
        - Positive skew: Longer/fatter tail on the right side (data spread more to the right).
        - Negative skew: Longer/fatter tail on the left side (data spread more to the left).
    
    SIMPLIFIED
        Kurtosis:
        Think of kurtosis as a way to measure how pointy or flat the top of a data graph is. 
        If the kurtosis is high, the graph has a sharp peak and long tails, meaning it has more extreme values. 
        If it's low, the graph is flatter at the top and doesn't have extreme values sticking out.

        Skewness:
        Skewness tells us if the data is tilted to one side. If skewness is positive, 
        the graph stretches more towards the right, showing more data on that side.
        If it's negative, it stretches more to the left. This helps us see if the data is evenly spread or if 
        it leans more one way.
"""

import datetime
import numpy as np
from scipy import stats
from colorama import Fore, init
import logging
from backend.job_assistant.gdrive import GoogleDriveManager
from backend.job_assistant.constants import (
    STATS_NUMBER_OFFERS_FILE_ID,
    STATS_SALARIES_FILE_ID,
)

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
        if job_title in json_data[date][self.api_name]:
            LOGGER.info(
                f"Salaries statistics already saved for API: {self.api_name} on {date}"
            )
            print(
                f"{Fore.YELLOW}Salaries statistics already saved for API: {self.api_name} on {date}"
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
        LOGGER.info(
            f"{Fore.GREEN}Salaries statistics stored for {job_title} for API: {self.api_name} on {date}"
        )

    def store_number_offers(self, job_title: str, number_offers: int) -> None:
        """
        Stores the number of job offers for a given job title on the current date, associated with a specific API.

        Args:
            job_title (str): The job title for which the number of offers is being recorded.
            number_offers (int): The number of offers to record.
        """
        json_data = self.gdrive_manager.read_json_file(STATS_NUMBER_OFFERS_FILE_ID)
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if date not in json_data:
            json_data[date] = {}
        if self.api_name not in json_data[date]:
            json_data[date][self.api_name] = {}
        if job_title in json_data[date][self.api_name]:
            LOGGER.info(
                f"Number offers for {job_title} already saved for API: {self.api_name} on {date}"
            )
            print(
                f"{Fore.YELLOW}Number offers for {job_title} already saved for API: {self.api_name} on {date}"
            )
            return

        json_data[date][self.api_name][job_title] = number_offers

        self.gdrive_manager.overwrite_json_file(json_data, STATS_NUMBER_OFFERS_FILE_ID)
        LOGGER.info(
            f"{Fore.GREEN}Number offers for {job_title} stored successfully for API: {self.api_name} on {date}"
        )
