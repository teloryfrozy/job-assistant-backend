"""
Scheduled task of Job Assistant
"""

import sys
import os

from backend.job_assistant.gdrive import GoogleDriveManager
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from backend.job_assistant.jobs_providers.reed_co_uk import ReedCoUk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.job_assistant.jobs_providers.adzuna import Adzuna
from backend.job_assistant.jobs_providers.findwork import FindWork
from backend.job_assistant.constants import ADZUNA, IT_JOBS, EXPERIENCE_LEVELS, REED_CO_UK

GOOGLE_DRIVE_MANAGER = GoogleDriveManager()


def adzuna_run():
    """Scan salaries data and save them for analytical purposes."""

    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ADZUNA)
    adzuna = Adzuna(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            job_title = f"{experience} {job}"
            adzuna.set_salaries_stats(job_title)


def find_work_run():
    """TODO: clean doc as a senior Python dev"""

    find_work = FindWork()
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            position = f"{experience} {job}".replace(" ", "+")
            find_work.set_total_results(position)


def reed_co_uk_run():
    """TODO: clean doc as a senior Python dev"""

    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, REED_CO_UK)
    reed_co_uk = ReedCoUk(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            job_title = f"{experience} {job}"
            reed_co_uk.set_salaries_stats(job_title)


def test_run():
    for i in range(10):
        print(f"Test n°{i}")
