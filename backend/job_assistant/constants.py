"""
Environment creds and others constants

TODO:
Constants defined here should be used in at least 2 differents files or they are secrets coming from .env file
Otherwise they should be defined locally
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# TODO: organize banner and constants
# TODO: create a FOLDER: "constants" and a file for job constants


######################## SECURITY ########################
root = Path(__file__).resolve().parent.parent.parent
env_path = root / ".env"
load_dotenv(dotenv_path=env_path)
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# --- Google Drive --- #
JSON_KEY_FILE = root / "gdrive_creds.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
STATS_SALARIES_FILE_ID = os.getenv("STATS_SALARIES_FILE_ID")
STATS_NUMBER_OFFERS_FILE_ID = os.getenv("STATS_NUMBER_OFFERS_FILE_ID")


# Job templates / typical jobs
EXPERIENCE_LEVELS = ["Intern", "Junior", "Senior"]
IT_JOBS = [
    "Full Stack Developer",
    "Network Administrator",
    "Software Engineer",
    "Cybersecurity Analyst",
    "Data Analyst",
]

######################## JOB OFFERS API ########################

# ----------------------- ADZUNA ----------------------- #
ADZUNA_API = "https://api.adzuna.com/v1/api/"
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_SECRET_KEY = os.getenv("ADZUNA_SECRET_KEY")
ADZUNA = "Adzuna"

# ----------------------- REED CO UK ----------------------- #
REED_CO_UK_SECRET_KEY = os.getenv("REED_CO_UK_SECRET_KEY")
REED_CO_UK = "ReedCoUk"

# ----------------------- FINDWORK ----------------------- #
FINDWORK_SECRET_KEY = os.getenv("FINDWORK_SECRET_KEY")


######################## ARTIFICIAL INTELLIGENCE ########################

# ----------------------- AWANLLM ----------------------- #
AWANLLM_SECRET_KEY = os.getenv("AWANLLM_SECRET_KEY")
