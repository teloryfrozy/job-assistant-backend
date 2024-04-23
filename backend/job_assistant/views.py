"""
Handles API calls to our rest api for now
"""

import json
from django.http import JsonResponse
from constants import ADZUNA_API, ADZUNA_APP_ID, ADZUNA_SECRET_KEY
import requests


def test(request):
    return JsonResponse({"message": "Test successful"})
