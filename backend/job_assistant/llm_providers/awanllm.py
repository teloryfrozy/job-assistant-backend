"""
TODO:
Handles Awan LLM Api calls

https://www.awanllm.com/models
"""

# All available models
# TODO: test prompt engineering and find the best for:
# CV analysis (skill summary)
# Job analysis (list of skills + xp and requirements)
# CV/Job matching



import requests
import json
from colorama import Fore, init

import sys
import os


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)


from backend.job_assistant.constants import AWANLLM_SECRET_KEY



init(autoreset=True)

url = "https://api.awanllm.com/v1/chat/completions"

model="Meta-Llama-3-8B-Instruct"

role = "assistant"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AWANLLM_SECRET_KEY}",
}

payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": role, "content": "Hello, Tell me about cloudFlare in 10 words"}
            ],
        }
    )
response = requests.request("POST", url, headers=headers, data=payload)
print(f"{Fore.GREEN}{response.json()}")