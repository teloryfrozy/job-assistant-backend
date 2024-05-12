"""
Reed.co.uk API calls

DOCUMENTATION
https://www.reed.co.uk/developers/jobseeker


TODO: clean description



# NEW API ADDDED!!!!
# TODO: exact same features as with ADZUNA in a separated file 💪
"""
import datetime
import json
import logging
import numpy as np
from scipy import stats
import requests
from .gdrive import GoogleDriveManager
from .constants import (
    REED_CO_UK_SECRET_KEY
)



######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)





import requests

# Define the API endpoint URL

# TODO: put in constant and import
api_url = "https://www.reed.co.uk/api/1.0/search"



# TODO: do not forget all the defined jobs in constants !! ONLY USE JOB TITLE THIS TIME !!
keywords = "Full Stack Developer"
api_key = REED_CO_UK_SECRET_KEY

# Construct the query parameters
params = {
    "fullTime": "true",
    "keywords": keywords,
}

# Make the request
response = requests.get(api_url, params=params, auth=(api_key, ''))

# Check if the request was successful
if response.status_code == 200:
    # Extract and print the response data
    data = response.json()

    countries = ["uk"]

    abs_min_salary = 1_000_000
    abs_max_salary = 0

    all_salaries = []

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
            
   
    
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.reason}")

















'''class ReedCoUk:

    def __init__(self) -> None:
        pass


    def set_stats(self, job: str, skills: list):

        def get_avg_salary_country(country: str) -> int:
            """
            Retrieves the average salary for a specific country.

            Args:
                country (str): Country code.

            Returns:
                int: Average salary.
            """
            url = f"{ADZUNA_API}jobs/{country}/jobsworth?"
            params = self.get_params({"title": job, "description": ",".join(skills)})

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                salary: int = data["salary"]
                return salary
            else:
                error_msg = f"Failed to retrieve average salary for country {country}. "
                error_msg += (
                    f"Status code: {response.status_code}, Reason: {response.reason}"
                )
                LOGGER.error(error_msg)
                return None

        gdrive_manager = GoogleDriveManager()
        json_data: dict = gdrive_manager.read_json_file(STATS_SALARIES_FILE_ID)

        data = {}
        countries = ["gb", "us"]
        all_salaries = []
        average = 0
        nb_success = 0
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not json_data.get(date):
            json_data[date] = {}

        for country in countries:
            result = get_avg_salary_country(country)
            if result:
                nb_success += 1
                average += result
                all_salaries.append(result)
                data[country] = result

        data["std_dev"] = int(np.std(all_salaries))
        data["kurtosis"] = float(stats.kurtosis(all_salaries))
        data["skewness"] = float(stats.skew(all_salaries))
        average = int(average / nb_success)
        data["avg"] = average

        json_data[date][job] = data
        gdrive_manager.overwrite_json_file(json_data, STATS_SALARIES_FILE_ID)'''