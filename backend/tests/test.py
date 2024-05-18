"""
THIS file is just for testing purpose to avoid the hassle of imports
"""

import json

import sys
import os

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.job_assistant.jobs_providers.adzuna import Adzuna
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager


from backend.job_assistant.gdrive import GoogleDriveManager

from backend.job_assistant.constants import (
    ADZUNA,
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
# the_muse_run()
# reed_co_uk_run()
# adzuna_run()


# ADZUNA
# IGNORE THIS FOR NOW
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
