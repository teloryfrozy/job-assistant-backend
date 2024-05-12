"""
Scheduled task of Job Assistant
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.job_assistant.adzuna import Adzuna
from backend.job_assistant.constants import JOBS_TEMPLATES


def adzuna_run():
    """Scan salaries data and save them for analytical purposes."""

    adzuna = Adzuna()
    for job in JOBS_TEMPLATES:
        for role in JOBS_TEMPLATES[job]:
            job_title = f"{role} {job}"
            skills = JOBS_TEMPLATES[job][role]
            adzuna.set_stats(job_title, skills)
            

def test_run():
    for i in range(10):
        print(f"Test n°{i}")

