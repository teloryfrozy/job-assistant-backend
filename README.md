<pre>
   __   ______   ______       ______   ______   ______   __   ______   ______  ______   __   __   ______  
  /\ \ /\  __ \ /\  == \     /\  __ \ /\  ___\ /\  ___\ /\ \ /\  ___\ /\__  _\/\  __ \ /\ "-.\ \ /\__  _\
 _\_\ \\ \ \/\ \\ \  __<     \ \  __ \\ \___  \\ \___  \\ \ \\ \___  \\/_/\ \/\ \  __ \\ \ \-.  \\/_/\ \/
/\_____\\ \_____\\ \_____\    \ \_\ \_\\/\_____\\/\_____\\ \_\\/\_____\  \ \_\ \ \_\ \_\\ \_\\"\_\  \ \_\
\/_____/ \/_____/ \/_____/     \/_/\/_/ \/_____/ \/_____/ \/_/ \/_____/   \/_/  \/_/\/_/ \/_/ \/_/   \/_/
</pre>

# JobAssistant

🔍 Job searching automated with AI | 🎯 Applying to jobs simplified
⚠️ Disclaimer: This project is no longer maintained. I created an API to normalize results from job posting APIs for statistical analysis. I connected it to Google Drive instead of hosting a database on a VPS, as I wanted to avoid additional costs. Feel free to use this project for inspiration, and you're welcome to submit pull requests to the repository.

## Table of Contents

- [JobAssistant](#jobassistant)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Limitations](#limitations)
  - [Get Started](#get-started)
    - [Clone the Repository](#clone-the-repository)
  - [🐋 Grant Execution Permissions and Start the Docker Container](#-grant-execution-permissions-and-start-the-docker-container)
  - [Modules](#modules)
    - [Resume Analyzer](#resume-analyzer)

## Introduction

JobAssistant is a powerful tool designed to automate the job search process using AI. It simplifies the application process, making it easier for users to find and apply to jobs that match their skills and preferences.

## Features

- **Automated Job Search:** Interacts with multiple job APIs to fetch job listings.
- **Resume Analysis:** Extracts and analyzes key information from resumes.
- **Statistical Analysis:** Computes job salary statistics using advanced statistical concepts like kurtosis and skewness.

## Limitations

- **Adzuna API:**
  - Only one endpoint available.
  - No custom API calls possible.
  - Only job offers in Germany in the tech industry.
- **FindWork API:**
  - No salary data provided.
- **The Muse API:**
  - Public API with no salary data provided.
  - Plenty of parameters available for job search.

## Get Started

### Clone the Repository

Replace `branchName` with the branch you want to clone (e.g., `main`):

```bash
git clone -b main https://github.com/teloryfrozy/job-assistant-backend
```

## 🐋 Grant Execution Permissions and Start the Docker Container

```bash
chmod +x start_backend.sh
sudo ./start_backend.sh
```

## Modules

### Resume Analyzer

This module extracts information from a PDF resume and utilizes a language model to assess the suitability of a job for a user by extracting relevant skills.

**Functions:**

- `extract_keywords(pdf_file_path: str) -> str`: Extracts keywords from a PDF file.
- `get_response(prompt: str) -> str`: Sends a prompt to an AI model and returns the generated response.
- `summarize_resume(keywords: str) -> dict`: Summarizes a resume by extracting relevant skills, experience, and education.

**Usage:**

## Setup credentials in a .env file at the root of the project
```bash
STATS_SALARIES_FILE_ID=""
STATS_NUMBER_OFFERS_FILE_ID=""

# JOB API KEYS
ADZUNA_SECRET_KEY=""
ADZUNA_APP_ID=""
REED_CO_UK_SECRET_KEY=""
FINDWORK_SECRET_KEY=""

# LLM API KEYS
AWANLLM_SECRET_KEY=""

DJANGO_SECRET_KEY = "django-insecure-u3uh8!@75!(v%p$+z%2%5--7uzc(+&e@wo=agw1io74#m)4%id"

# GOOGLE DRIVE SERVICE CREDS
GDRIVE_TYPE = "service_account"
GDRIVE_PROJECT_ID = ""
GDRIVE_PRIVATE_KEY_ID = ""
GDRIVE_PRIVATE_KEY = ""
GDRIVE_CLIENT_EMAIL = ""
GDRIVE_CLIENT_ID = ""
GDRIVE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GDRIVE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GDRIVE_AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
GDRIVE_CLIENT_X509_CERT_URL = ""
GDRIVE_UNIVERSE_DOMAIN = "googleapis.com"
```

1. Extract text from a PDF resume using `extract_keywords`.
2. Summarize the resume to identify relevant skills and experiences using `summarize_resume`.
3. Utilize the extracted data to assess the closeness of a job to the user's profile.
