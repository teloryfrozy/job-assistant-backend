"""
THIS file is just for testing purpose to avoid the hassle of imports
"""

# VERY IMPORTANT
# https://developers.greenhouse.io/job-board.html#submit-an-application
# => submit via an API


import json

import sys
import os

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from backend.job_assistant.gdrive import GoogleDriveManager

from backend.job_assistant.constants import (
    AWANLLM_SECRET_KEY,
    EXPERIENCE_LEVELS,
    FINDWORK_SECRET_KEY,
    IT_JOBS,
    REED_CO_UK_SECRET_KEY,
    STATS_SALARIES_FILE_ID,
)


GOOGLE_DRIVE_MANAGER = GoogleDriveManager()

from backend.core.cron import adzuna_run, reed_co_uk_run, find_work_run, the_muse_run

# find_work_run()
the_muse_run()
# reed_co_uk_run()
# adzuna_run()



url = "https://www.themuse.com/api/search-renderer/jobs?ctsEnabled=true&query=Full Stack Developer&level=internship,entry,mid,senior,management&category=software_engineering,computer_it&posted_date_range=last_30d"


response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    number_offers = data["count"]
    print(number_offers)
else:
    # TODO: LOGGER.ERROR
    print(f"Error: {response.status_code} - {response.reason}")



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
