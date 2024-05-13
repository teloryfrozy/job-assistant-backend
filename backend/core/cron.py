"""
Scheduled task of Job Assistant
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.job_assistant.adzuna import Adzuna
from backend.job_assistant.findwork import FindWork
from backend.job_assistant.constants import IT_JOBS, EXPERIENCE_LEVELS


def adzuna_run():
    """Scan salaries data and save them for analytical purposes."""

    adzuna = Adzuna()
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            job_title = f"{experience} {job}"
            adzuna.set_stats(job_title)


def find_work_run():
    """TODO"""

    find_work = FindWork()
    for job in IT_JOBS:
        for experience in EXPERIENCE_LEVELS:
            position = f"{experience} {job}".replace(" ", "+")
            find_work.set_total_results(position)


def test_run():
    for i in range(10):
        print(f"Test n°{i}")
