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

from backend.core.cron import adzuna_run, reed_co_uk_run, find_work_run

# find_work_run()
# reed_co_uk_run()
# adzuna_run()


# ONLY FOR JOB SEARCH
# FREE API: no parameters (ONLY JOB OFFERS IN GERMAN)
"""
url = "https://www.arbeitnow.com/api/job-board-api"
"""

# ONLY FOR JOB SEARCH - NO SALARY PROVIDED => can still be used for stats
# FREE API: no parameters => need to be checked with a loop
# doc: https://www.themuse.com/developers/api/v2

# https://www.themuse.com/api/public/jobs?category=Account%20Management&category=IT&level=Entry%20Level&level=Senior%20Level&page=1
"""
url = "https://www.themuse.com/api/public/jobs?category=Accounting&page=1"
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
