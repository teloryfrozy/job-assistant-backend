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
