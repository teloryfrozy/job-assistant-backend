<pre>
   __   ______   ______       ______   ______   ______   __   ______   ______  ______   __   __   ______  
  /\ \ /\  __ \ /\  == \     /\  __ \ /\  ___\ /\  ___\ /\ \ /\  ___\ /\__  _\/\  __ \ /\ "-.\ \ /\__  _\ 
 _\_\ \\ \ \/\ \\ \  __<     \ \  __ \\ \___  \\ \___  \\ \ \\ \___  \\/_/\ \/\ \  __ \\ \ \-.  \\/_/\ \/ 
/\_____\\ \_____\\ \_____\    \ \_\ \_\\/\_____\\/\_____\\ \_\\/\_____\  \ \_\ \ \_\ \_\\ \_\\"\_\  \ \_\ 
\/_____/ \/_____/ \/_____/     \/_/\/_/ \/_____/ \/_____/ \/_/ \/_____/   \/_/  \/_/\/_/ \/_/ \/_/   \/_/ 
</pre>


# JobAssistant

🔍 Job searching automated with AI | 🎯 Applying to jobs simplified

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
git clone -b branchName https://your_pseudo:token@github.com/Zapony/JobAssistant
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

1. Extract text from a PDF resume using `extract_keywords`.
2. Summarize the resume to identify relevant skills and experiences using `summarize_resume`.
3. Utilize the extracted data to assess the closeness of a job to the user's profile.
