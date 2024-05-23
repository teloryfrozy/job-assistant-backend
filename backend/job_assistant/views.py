"""
TODO: clean doc as a senior Python developer with 20 years of experience
Handles API calls to our rest api for now
"""

import json
from rest_framework import status
import logging
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from backend.job_assistant.constants import (
    ADZUNA,
    ARBEIT_NOW,
    FINDWORK,
    REED_CO_UK,
    THE_MUSE,
)
from backend.job_assistant.gdrive import GoogleDriveManager
from backend.job_assistant.jobs_providers.adzuna import Adzuna
from backend.job_assistant.jobs_providers.arbeitnow import ArbeitNow
from backend.job_assistant.jobs_providers.findwork import FindWork
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from backend.job_assistant.jobs_providers.reed_co_uk import ReedCoUk
from backend.job_assistant.jobs_providers.the_muse import TheMuse

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
def test(request):
    return JsonResponse({"message": "Test successful"})


@api_view(["POST"])
def get_jobs_arbeit_now(request: HttpRequest):
    """
    TODO
    """
    parameters: dict = json.loads(request.body)
    visa_sponsorship = parameters.get("visa_sponsorship")

    GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ARBEIT_NOW)

    jobs_offers = {}
    arbeit_now = ArbeitNow(job_statistics_manager)

    arbeit_now_job_offers = arbeit_now.get_jobs(visa_sponsorship)
    jobs_offers[ARBEIT_NOW] = arbeit_now_job_offers


    return JsonResponse({"offers": arbeit_now_job_offers}, status=status.HTTP_200_OK)

@api_view(["POST"])
def get_jobs(request: HttpRequest):
    """
    TODO
    """
    parameters: dict = json.loads(request.body)

    # TODO: review all jobs providers docs and add ALL possible params
    job_title: str = parameters["job_title"]
    jobs_providers: list = parameters["jobs_providers"]
    level: str = parameters.get("level")
    # sort_by:str = data["sortBy"]
    skills: list = parameters.get("skills")
    location: dict = parameters.get("location")
    if location:
        city: str = location.get("city")
        country: str = location.get("country")
    min_salary: int = parameters.get("min_salary")
    max_salary: int = parameters.get("max_salary")
    full_time: bool = parameters.get("full_time")
    permanent: bool = parameters.get("permanent")
    remote: bool = parameters.get("remote")
    number_offers: int = parameters.get(
        "number_offers"
    )  # just to be quicker if poor connection

    jobs_offers = {}

    GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ADZUNA)

    # TODO: USE functions to split the code
    ####################################################
    if ADZUNA in jobs_providers:
        job_statistics_manager.api_name = ADZUNA
        adzuna = Adzuna(job_statistics_manager)

        params = {
            "what": job_title,
            # "where": city,
            # "sort_by": "salary",
            "salary_min": min_salary,
        }
        if full_time:
            params["full_time"] = 1
        if permanent:
            params["permanent"] = 1

        adzuna_job_offers = adzuna.get_jobs(country, params)
        jobs_offers[ADZUNA] = adzuna_job_offers

    ####################################################

    if FINDWORK in jobs_providers:
        job_statistics_manager.api_name = FINDWORK
        find_work = FindWork(job_statistics_manager)

        # TODO: add clean params instead of hard coding
        params = {
            "employment_type": "full time",
            "remote": "false",
            "location": "New York",
            "search": "ethereum web3",
        }

        find_work_job_offers = find_work.get_jobs(params)
        jobs_offers[FINDWORK] = find_work_job_offers
    ####################################################
    if REED_CO_UK in jobs_providers:
        job_statistics_manager.api_name = REED_CO_UK
        reed_co_uk = ReedCoUk(job_statistics_manager)

        params = {
            "keywords": job_title,
            "minimumSalary": min_salary,
            "fullTime": full_time,
            "locationName": country,
        }

        reed_co_uk_job_offers = reed_co_uk.get_jobs(params)
        jobs_offers[REED_CO_UK] = reed_co_uk_job_offers
    ####################################################
    if THE_MUSE in jobs_providers:
        job_statistics_manager.api_name = THE_MUSE
        the_muse = TheMuse(job_statistics_manager)

        params = {
            "query": job_title,
            "level": level,
            "category": [
                # "Computer and IT",
                # "Data and Analytics",
                # "Data Science",
                "Design and UX",
                # "IT",
                # "Software Engineer",
                # "Software Engineering",
            ],
            # "level": ["Senior Level", "Internship"],
            "location": ["London, United Kingdom", "Paris, France"],
        }

        the_muse_job_offers = the_muse.get_jobs(params)
        jobs_offers[THE_MUSE] = the_muse_job_offers
    ####################################################
    return JsonResponse({"offers": jobs_offers}, status=status.HTTP_200_OK)
