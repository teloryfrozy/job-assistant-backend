"""
TODO:
Handles Awan LLM Api calls

https://www.awanllm.com/models




# TODO: Create prompt engineering for:
# CV analysis (skill summary)
# Job analysis (list of skills + xp and requirements)
# CV/Job matching


IDEA:
add tools to the ai such as checking the number of github contributions to verify if skills are valid
"""

import re
import requests
import json
from colorama import Fore, init

import sys
import os


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)


from backend.job_assistant.constants import (
    AWANLLM_SECRET_KEY,
)

AWANLLM_API = "https://api.awanllm.com/v1/chat/completions"
MODEL = "Meta-Llama-3-8B-Instruct"
ROLE = "assistant"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AWANLLM_SECRET_KEY}",
}

init(autoreset=True)


def get_response(prompt: str) -> str:
    """
    Get response from an AI model based on the provided prompt.

    Args:
        prompt (str): The prompt to be sent to the AI model.

    Returns:
        str: The response generated by the AI model.
    """
    payload = json.dumps(
        {"model": MODEL, "messages": [{"role": ROLE, "content": prompt}]}
    )

    response = requests.post(AWANLLM_API, headers=HEADERS, data=payload)
    json_data = response.json()
    clear_text = json_data["choices"][0]["message"]["content"]

    return clear_text


def summarize_resume(keywords: str) -> dict:
    """
    Summarizes a resume by sending a request to an API.

    Args:
        keywords (str): Text extracted from resume.

    Returns:
        dict: Extracted information from the resume in JSON format.
    """

    template = f"""
    As a smart recruiter assistant specialized in CV analysis.
    1) Analyse the following CV of an applicant
    2) Extract the most relevant skills, experience and education.
    4) Ignore all unnecessary details (e.g: phone number, email address, birthday)

    Extracted applicant information from its CV:
    {keywords}

    ---
    Do NOT explain your thinking process. Do not add additional informations and details
    Answer MUST be a Json format matching this template:
    {{
        "skills": {{
            "hard": [dev stack and technologies used],
            "soft": []
        }},
        "experience": {{
            "pro": [
                "experience1": [very brief list of tasks],
                ...,
                "experienceN": [very brief list of tasks]
            ],
            "perso": [
                "experience1": [very brief list of tasks],
                ...,
                "experienceN": [very brief list of tasks]
            ]
        }},
        "education": {{
            "university": "",
            "degrees": []
        }}
    }}
    """
    clear_text = get_response(template)
    print(f"{Fore.GREEN}============ DEBUGGING RESUME SUMMARY ============")
    print(f"{Fore.YELLOW}{clear_text}")

    pattern = r"```(.*?)```"
    matches = re.findall(pattern, clear_text, re.DOTALL)

    if matches:
        user_data = json.loads(matches[0])
    else:
        json_text = clear_text.split("JSON format:", 1)[-1].strip()
        user_data = json.loads(json_text)

    return user_data
