"""
TODO: clean doc as a senior Python developer with 20 years of experience
Handles API calls to our rest api for now
"""

import json
from rest_framework import status
import logging
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from backend.job_assistant.constants import ADZUNA, FINDWORK
from backend.job_assistant.gdrive import GoogleDriveManager
from backend.job_assistant.jobs_providers.adzuna import Adzuna
from backend.job_assistant.jobs_providers.findwork import FindWork
from backend.job_assistant.jobs_providers.job_statistics import JobStatisticsManager

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
def test(request):
    return JsonResponse({"message": "Test successful"})


@api_view(["POST"])
def get_jobs(request: HttpRequest):
    parameters: dict = json.loads(request.body)

    # TODO: review all jobs providers docs and add ALL possible params
    job_title: str = parameters["job_title"]
    jobs_providers: list = parameters["jobs_providers"]
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
    remote: bool =parameters.get("remote")
    number_offers: int = parameters.get(
        "numberOffers"
    )  # just to be quicker if poor connection


    
    jobs_offers = {}
    # TODO get all params and redirect to the correct APIs providers

    ############# ONLY FOR ADZUNA ########################
    if ADZUNA in jobs_providers:

        GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
        # no need to recreate a JobStatisticsManager => just change the api_name for logging purposes
        job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ADZUNA)


        params = {
            "what": job_title,
            "where": location,
            "sort_by": "salary",
            "salary_min": min_salary,
            "full_time": 1,
            "permanent": 1,
        }


        adzuna = Adzuna(job_statistics_manager)
        adzuna_job_offers = adzuna.get_jobs("gb", params)
        jobs_offers[ADZUNA] = adzuna_job_offers

    ####################################################

    if FINDWORK in jobs_providers:

        
        GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
        job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, FINDWORK)


        # no need to recreate a JobStatisticsManager => just change the api_name for logging purposes
        #job_statistics_manager.api_name = FINDWORK
        find_work = FindWork(job_statistics_manager)


        params = {
            "employment_type": "full time",
            "remote": "false",
            "location": "New York",
            "search": "ethereum web3",
        }

        find_work_job_offers = find_work.get_jobs(params)
        jobs_offers[FINDWORK] = find_work_job_offers


    return JsonResponse({"offers": jobs_offers}, status=status.HTTP_200_OK)
