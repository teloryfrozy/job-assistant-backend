"""
TODO: clean doc as a senior Python developer with 20 years of experience
Handles API calls to our rest api for now
"""

import json
from rest_framework import status
import logging
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from job_assistant import pdf_manager
from job_assistant.constants import (
    ADZUNA,
    ARBEIT_NOW,
    FINDWORK,
    REED_CO_UK,
    THE_MUSE,
)
from job_assistant.gdrive import GoogleDriveManager
from job_assistant.jobs_providers.adzuna import Adzuna
from job_assistant.jobs_providers.arbeitnow import ArbeitNow
from job_assistant.jobs_providers.findwork import FindWork
from job_assistant.jobs_providers.job_statistics import JobStatisticsManager
from job_assistant.jobs_providers.reed_co_uk import ReedCoUk
from job_assistant.jobs_providers.the_muse import TheMuse
from job_assistant.llm_providers import awanllm

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
def test(request):
    return JsonResponse({"message": "Test successful"})


@api_view(["POST"])
def analyze_cv(request: HttpRequest):
    """
    Analyzes a CV from a PDF file, extracting keywords and summarizing the content using AI.

    Expects:
        Content-Type: application/pdf
        Body: PDF file content

    Responses:
        200 OK: Successfully processed the CV.
        400 Bad Request: Unsupported file type or file too large.
        500 Internal Server Error: Error during CV analysis.
    """
    try:
        content_type = request.headers.get("Content-Type")
        if content_type != "application/pdf":
            LOGGER.error(f"Unsupported file type: {content_type}")
            return JsonResponse(
                {"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST
            )

        file_content = request.body

        # Check file size (10MB = 10 * 1024 * 1024 bytes)
        max_size = 10 * 1024 * 1024
        if len(file_content) > max_size:
            LOGGER.error(f"File too large: {len(file_content)} bytes")
            return JsonResponse(
                {"error": "File too large"}, status=status.HTTP_400_BAD_REQUEST
            )

        keywords = pdf_manager.extract_keywords_from_bytes(file_content)

        try:
            user_data = awanllm.summarize_resume(keywords)
        except json.JSONDecodeError as e:
            return JsonResponse(
                {"error": "AI failed to return a proper JSON format"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"An error occurred during CV analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # TODO: save keywords in database

        LOGGER.info("Keywords extracted and saved from CV successfully")
        return JsonResponse(
            {
                "message": "Keywords extracted and saved from CV successfully",
                "extracted_data": user_data,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.exception(f"An error occurred during CV analysis: {str(e)}")
        return JsonResponse(
            {"error": f"An error occurred during CV analysis: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_top_companies(request: HttpRequest):
    """
    Get the top companies for a specific country and job category.

    Parameters:
        - request (HttpRequest): The HTTP request object containing the country and category parameters.

    Returns:
        JsonResponse: A JSON response containing the top companies or an error message.
    """
    parameters: dict = json.loads(request.body)
    country: str = parameters.get("country")
    category: str = parameters.get("category")

    if not country:
        return JsonResponse(
            {"error": "Country is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not category:
        return JsonResponse(
            {"error": "Category is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    top_companies = Adzuna().get_top_companies(country, category)
    if isinstance(top_companies, list):
        return JsonResponse({"top_companies": top_companies}, status=status.HTTP_200_OK)
    else:
        return JsonResponse(
            {"error": top_companies}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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
    TODO: clean doc as a senior Python developer with 20 years of experience of that function get_jobs
    """
    parameters: dict = json.loads(request.body)

    # TODO: review all jobs providers docs and add ALL possible params

    job_title: str = parameters["job_title"]
    jobs_providers: list = parameters["jobs_providers"]
    level: str = parameters.get("level")
    skills: list = parameters.get("skills")
    location: dict = parameters.get("location")
    if location:
        city: str = location.get("city")
        country: str = location.get("country")
    min_salary: int = parameters.get("min_salary")
    max_salary: int = parameters.get("max_salary")
    max_days_old: int = parameters.get("max_days_old")
    full_time: bool = parameters.get("full_time")
    permanent: bool = parameters.get("permanent")
    contract: bool = parameters.get("contract")
    part_time: bool = parameters.get("part_time")
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
            "salary_min": min_salary,
            "salary_max": max_salary,
        }

        if contract:
            params["contract"] = 1
        if full_time:
            params["full_time"] = 1
        if permanent:
            params["permanent"] = 1
        if part_time:
            params["part_time"] = 1

        adzuna_job_offers = adzuna.get_jobs(country, params)
        if isinstance(adzuna_job_offers, dict):
            jobs_offers[ADZUNA] = adzuna_job_offers

    ####################################################

    if FINDWORK in jobs_providers:
        job_statistics_manager.api_name = FINDWORK
        find_work = FindWork(job_statistics_manager)

        params = {}
        if full_time:
            params["employment_type"] = "full time"
        if contract:
            params["employment_type"] = "contract"
        if part_time:
            params["employment_type"] = "contract"
        if remote:
            params["remote"] = "true"
        if location:
            if country:
                params["location"] = country
                if city:
                    params["location"] += f", {city}"
            elif city:
                params["location"] = city
        params["search"] = job_title

        find_work_job_offers = find_work.get_jobs(params)
        if isinstance(find_work_job_offers, dict):
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
