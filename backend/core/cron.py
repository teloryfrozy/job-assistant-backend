"""
Scheduled Task of Job Assistant

This module is designed to interact with various job providers to collect and analyze job market data.
It utilizes specific classes for different job providers to fetch data related to IT jobs and their respective salaries
and number of offers based on experience levels. The collected data is managed and stored using Google Drive.
"""

from job_assistant.gdrive import GoogleDriveManager
from job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from job_assistant.jobs_providers.reed_co_uk import ReedCoUk
from job_assistant.jobs_providers.adzuna import Adzuna
from job_assistant.jobs_providers.findwork import FindWork
from job_assistant.constants import (
    ADZUNA,
    FINDWORK,
    IT_JOBS,
    EXPERIENCE_LEVELS,
    REED_CO_UK,
    THE_MUSE,
)
from job_assistant.jobs_providers.the_muse import TheMuse

GOOGLE_DRIVE_MANAGER = GoogleDriveManager()


def dummy_task():
    print("Hello from dummy task!")


def collect_job_data():
    """
    Runs all scheduled tasks to collect and store job market data.
    """
    adzuna_run()
    reed_co_uk_run()
    find_work_run()
    the_muse_run()


def adzuna_run():
    """
    Collects and stores salary statistics from Adzuna for IT jobs at various experience levels
    """
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ADZUNA)
    adzuna = Adzuna(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            job_title = f"{experience} {job}"
            adzuna.set_salaries_stats(job_title)
            adzuna.set_number_offers(
                country="fr",
                params={
                    "max_days_old": 7,
                    "what_and": experience,
                    "title_only": job,
                    "full_time": 1,
                    "permanent": 1,
                },
            )


def reed_co_uk_run():
    """
    Collects and stores salary statistics from Reed.co.uk for IT jobs at various experience levels.
    """
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, REED_CO_UK)
    reed_co_uk = ReedCoUk(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            job_title = f"{experience} {job}"
            reed_co_uk.set_salaries_stats(job_title)
            reed_co_uk.set_number_offers(job_title)


def find_work_run():
    """
    Collects and stores the number of job offers from FindWork for IT jobs at various experience levels.
    """
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, FINDWORK)
    find_work = FindWork(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            position = f"{experience} {job}"
            find_work.set_number_offers(position)


def the_muse_run():
    """
    Collects and stores the number of job offers from The Muse for IT jobs at various experience levels.
    """
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, THE_MUSE)
    the_muse = TheMuse(job_statistics_manager)
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            the_muse.set_number_offers(job, experience)
