"""
THIS file is just for testing purpose to avoid the hassle of imports
"""

# VERY IMPORTANT
# https://developers.greenhouse.io/job-board.html#submit-an-application
# => submit via an API


import json
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from backend.job_assistant.constants import (
    AWANLLM_SECRET_KEY,
    EXPERIENCE_LEVELS,
    FINDWORK_SECRET_KEY,
    IT_JOBS,
    REED_CO_UK_SECRET_KEY,
)
from backend.core.cron import adzuna_run


# adzuna_run()


# ONLY FOR JOB SEARCH - NO SALARY PROVIDED => can still be used for stats
# FREE API: no parameters => need to be checked with a loop
"""
url = "https://www.arbeitnow.com/api/job-board-api"
"""

# ONLY FOR JOB SEARCH - NO SALARY PROVIDED => can still be used for stats
# FREE API: no parameters => need to be checked with a loop
# doc: https://www.themuse.com/developers/api/v2
"""
url = "https://www.themuse.com/api/public/jobs?category=Accounting&page=1"
"""


# THIS CODE IS USED TO SEE HOW DATA LOOKS LIKE WITH REED.CO.UK

"""import requests

# Define the API endpoint URL
api_url = "https://www.reed.co.uk/api/1.0/search"

# Define your search parameters
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
            
   
    print(json.dumps(data["results"], indent=4))
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.reason}")
"""

# ADZUNA
# IGNORE THIS FOR NOW
"""
results = Request.get_jobs(
    country="gb",
    params={
        "results_per_page": 20,
        "what": "javascript developer",
        "what_exclude": "java",
        "where": "london",
        "sort_by": "salary",
        "salary_min": 30000,
        "full_time": 1,
        "permanent": 1,
    },
    nb_pages=2,
)
"""


# for json_data in results:
#     print(json.dumps(json_data, indent=4))


"""response = Request.get_jobs(
    country="gb",
    params={
        "results_per_page": 20,
        "what": "javascript developer",
        "what_exclude": "java",
        "where": "london",
        "sort_by": "salary",
        "salary_min": 30000,
        "full_time": 1,
        "permanent": 1,
    },
    nb_pages=2,
)

json_data = response.json()


#This code is just to play around and check
for result in json_data["results"]:
    print(result["id"])
    print(result["title"])
    print(result["description"])
    print(f"location: {result['location']['display_name']}")
    print(f"category: {result['category']['label']}")
    print(f"company: {result['company']['display_name']}")
    print(f"URL: {result['redirect_url']}")
    print(f"Poste: {result['created']}")
    print("\n\n")"""
