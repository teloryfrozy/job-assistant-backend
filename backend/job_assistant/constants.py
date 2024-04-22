"""
Environment creds and others constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv




######################## SECURITY ########################
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")




######################## JOB OFFERS API ########################
ADZUNA_API = "https://api.adzuna.com/v1/api/"
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_SECRET_KEY = os.getenv("ADZUNA_SECRET_KEY")
