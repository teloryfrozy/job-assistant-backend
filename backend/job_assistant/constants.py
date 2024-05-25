"""
Environment creds and others constants

TODO:
Constants defined here should be used in at least 2 differents files or they are secrets coming from .env file
Otherwise they should be defined locally
"""

import os

# TODO: organize banner and constants
# TODO: create a FOLDER: "constants" and a file for job constants


######################## SECURITY ########################
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# --- Google Drive --- #
GDRIVE_SERVICE_CREDS = {
    "type": os.getenv("GDRIVE_TYPE"),
    "project_id": os.getenv("GDRIVE_PROJECT_ID"),
    "private_key_id": os.getenv("GDRIVE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GDRIVE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("GDRIVE_CLIENT_EMAIL"),
    "client_id": os.getenv("GDRIVE_CLIENT_ID"),
    "auth_uri": os.getenv("GDRIVE_AUTH_URI"),
    "token_uri": os.getenv("GDRIVE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GDRIVE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GDRIVE_CLIENT_X509_CERT_URL"),
}
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
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_SECRET_KEY = os.getenv("ADZUNA_SECRET_KEY")
ADZUNA = "Adzuna"

# ----------------------- REED CO UK ----------------------- #
REED_CO_UK_SECRET_KEY = os.getenv("REED_CO_UK_SECRET_KEY")
REED_CO_UK = "ReedCoUk"

# ----------------------- FINDWORK ----------------------- #
FINDWORK_SECRET_KEY = os.getenv("FINDWORK_SECRET_KEY")
FINDWORK = "Findwork"

# ----------------------- The Muse ----------------------- #
THE_MUSE = "TheMuse"

# ----------------------- Arbeit Now ----------------------- #
ARBEIT_NOW = "ArbeitNow"


######################## ARTIFICIAL INTELLIGENCE ########################

# ----------------------- AWANLLM ----------------------- #
AWANLLM_SECRET_KEY = os.getenv("AWANLLM_SECRET_KEY")
