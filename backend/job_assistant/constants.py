"""
Environment creds and others constants
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


# Job template / typical jobs
# TODO: read and check if skills are relevant
JOBS_TEMPLATES = {
    "Full Stack Developer": {
        "Intern": ["HTML", "CSS", "JavaScript"],
        "Junior": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Django",
            "React",
            "Git",
            "Testing",
        ],
        "Senior": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Django",
            "React",
            "Git",
            "Testing",
            "Node.js",
            "SQL",
            "DevOps",
            "AWS",
            "Azure",
        ],
    },
    "Network Administrator": {
        "Intern": ["IP", "Switch", "Routing", "Virtualization"],
        "Junior": [
            "IP",
            "Switch",
            "Routing",
            "Virtualization",
            "CCNA3",
            "Monitoring",
            "Active Directory",
        ],
        "Senior": [
            "IP",
            "Switch",
            "Routing",
            "Virtualization",
            "CCNA3",
            "Monitoring",
            "Active Directory",
            "Network Automation",
            "TCP",
            "UDP",
            "Cloud",
            "Backup",
            "WLAN",
            "Powershell",
        ],
    },
    "Software Engineer": {
        "Intern": ["Python", "Java", "Data Structures", "Algorithms"],
        "Junior": [
            "Python",
            "Java",
            "Data Structures",
            "Algorithms",
            "Python",
            "Java",
            "C++",
            "Testing",
        ],
        "Senior": [
            "Python",
            "Java",
            "C++",
            "Testing",
            "System Design",
            "Software Architecture",
            "Agile",
            "Mentorship",
            "PostgreSQL",
            "Oracle",
            "MariaDB",
        ],
    },
    "Cybersecurity Analyst": {
        "Intern": ["Network", "Phishing", "PRTG"],
        "Junior": ["Network", "Phishing", "PRTG", "SIEM", "Scanning", "Solarwinds"],
        "Senior": [
            "Network",
            "Phishing",
            "PRTG",
            "SIEM",
            "Scanning",
            "Solarwinds",
            "NIST",
            "Penetration Testing",
            "Cloud Security",
            "Security Audits",
        ],
    },
    "Data Analyst": {
        "Intern": ["Excel", "Data Cleaning", "Data Visualization", "Tableau"],
        "Junior": [
            "Excel",
            "Data Cleaning",
            "Data Visualization",
            "Tableau",
            "Pandas",
            "Numpy",
            "SQL",
            "Python",
            "Data Wrangling",
            "Data Visualization",
            "Data Warehousing",
            "Machine Learning",
        ],
        "Senior": [
            "Excel",
            "Data Cleaning",
            "Data Visualization",
            "Tableau",
            "Pandas",
            "Numpy",
            "SQL",
            "Python",
            "Data Wrangling",
            "Data Visualization",
            "Data Warehousing",
            "Machine Learning",
            "Statistics",
            "Spark",
            "Hadoop",
            "Data Modeling",
            "Deep Learning",
        ],
    },
}


######################## JOB OFFERS API ########################

######################## ADZUNA ########################
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

######################## REED CO UK ########################
REED_CO_UK_SECRET_KEY = os.getenv("REED_CO_UK_SECRET_KEY")
