"""

TODO: clean file header description


Reed.co.uk API calls

DOCUMENTATION
https://www.reed.co.uk/developers/jobseeker


"""

import logging
import requests
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from backend.job_assistant.constants import REED_CO_UK_SECRET_KEY


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


API_URL = "https://www.reed.co.uk/api/1.0/search"


class ReedCoUk:
    """
    Class for interacting with the Reed CO UK API and performing statistical analysis on job salaries.
    """

    def __init__(self, job_statistics_manager: JobStatisticsManager) -> None:
        self.job_statistics_manager = job_statistics_manager

    def set_salaries_stats(self, job_title: str):
        """
        Retrieves job statistics including average salary, standard deviation, kurtosis, and skewness, min and max
        based on job title.

        Args:
            job_title (str): Job title.
        """
        params = {
            "fullTime": "true",
            "keywords": job_title,
        }

        response = requests.get(
            API_URL, params=params, auth=(REED_CO_UK_SECRET_KEY, "")
        )

        if response.status_code == 200:
            data = response.json()
            all_salaries = []
            abs_min_salary = 1_000_000
            abs_max_salary = 0

            for job in data["results"]:
                max_salary = job["maximumSalary"]
                min_salary = job["minimumSalary"]
                if max_salary is not None and min_salary is not None:
                    # sometimes salary is the pay per day
                    if max_salary > 10_000 and min_salary > 10_000:
                        all_salaries.append(max_salary)
                        all_salaries.append(min_salary)

                        if max_salary > abs_max_salary:
                            abs_max_salary = max_salary
                        if min_salary < abs_min_salary:
                            abs_min_salary = min_salary

                        if max_salary and min_salary:
                            all_salaries.extend([max_salary, min_salary])

            if all_salaries:
                self.job_statistics_manager.store_salaries_statistics(
                    job_title, all_salaries, abs_min_salary, abs_max_salary
                )
            else:
                LOGGER.error("No salary data available for the given job title.")
        else:
            LOGGER.error(
                f"Failed to retrieve data: {response.status_code} - {response.reason}"
            )
