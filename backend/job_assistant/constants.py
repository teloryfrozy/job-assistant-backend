"""
Environment creds and others constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# TODO: organize banner and constants


######################## SECURITY ########################
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# --- Google Drive --- # 
JSON_KEY_FILE = "gdrive_creds.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
STATS_SALARIES_FILE_ID = os.getenv("STATS_SALARIES_FILE_ID")



######################## JOB OFFERS API ########################
ADZUNA_API = "https://api.adzuna.com/v1/api/"
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_SECRET_KEY = os.getenv("ADZUNA_SECRET_KEY")
ADZUNA_COUNTRY_EXTENSIONS = [
    "gb",
    "us",
    "at",
    "au",
    "be",
    "br",
    "ca",
    "ch",
    "de",
    "es",
    "fr",
    "in",
    "it",
    "mx",
    "nl",
    "nz",
    "pl",
    "sg",
    "za",
]
