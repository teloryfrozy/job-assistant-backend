"""
TODO: clean doc as a senior Python developer with 20 years of experience
Handles API calls to our rest api for now
"""

import json
from rest_framework import status
import logging
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
def test(request):
    return JsonResponse({"message": "Test successful"})


@api_view(["POST"])
def get_jobs(request: HttpRequest):
    data: dict = json.loads(request.body)

    job_title: str = data["jobTitle"]
    skills: list = data.get("skills")
    location: dict = data.get("location")
    if location:
        city: str = location.get("city")
        country: str = location.get("country")
    min_salary: int = data.get("minSalary")
    max_salary: int = data.get("maxSalary")
    full_time: bool = data.get("fullTime")
    permanent: bool = data.get("permanent")
    number_offers: int = data.get(
        "numberOffers"
    )  # just to be quicker if poor connection

    # TODO get all params and redirect to the correct APIs providers

    jobs_offers = []

    return JsonResponse({"offers": jobs_offers}, status=status.HTTP_200_OK)
