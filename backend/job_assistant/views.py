"""
Handles API calls to our rest api for now
"""

import json
from django.http import JsonResponse
from constants import ADZUNA_API, ADZUNA_APP_ID, ADZUNA_SECRET_KEY
import requests


def test(request):
    return JsonResponse({"message": "Test successful"})


def get_jobs(query: str) -> requests.Response:
    """Builds the URL with the credentials."""
    url = f"{ADZUNA_API}{query}?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_SECRET_KEY}"
    hdr = {"Accept": "application/json"}
    return requests.get(url, headers=hdr)


response = get_jobs("jobs/gb/search/1")
json_data = response.json()

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))
