"""
TODO: clean doc as a senior Python developer with 20 years of experience
Handles API calls to our rest api for now
"""

import json
import threading
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

    This endpoint processes the following request parameters:
    - country (str): The country for which to retrieve the top companies.
    - category (str): The job category for which to retrieve the top companies.

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
    Handle job search requests by querying the ArbeitNow job provider and returning the results.

    This endpoint processes the following request parameters:
    - visa_sponsorship (optional): Filters jobs based on visa sponsorship availability.

    Returns a JSON response containing job offers from the ArbeitNow job provider.
    """
    parameters: dict = json.loads(request.body)
    visa_sponsorship = parameters.get("visa_sponsorship")

    GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
    job_statistics_manager = JobStatisticsManager(
        GOOGLE_DRIVE_MANAGER, ARBEIT_NOW)

    arbeit_now = ArbeitNow(job_statistics_manager)
    arbeit_now_job_offers = arbeit_now.get_jobs(visa_sponsorship)

    jobs_offers = {ARBEIT_NOW: arbeit_now_job_offers}

    return JsonResponse({"offers": jobs_offers}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jobs(request: HttpRequest):
    """
    Handle job search requests by querying multiple job providers and aggregating the results.

    This endpoint processes the following request parameters:
    - job_title (str): The title of the job to search for.
    - jobs_providers (list): List of job providers to query.
    - level (list, optional): List of experience levels to filter by.
    - skills (list, optional): List of skills to filter by.
    - max_days_old (int, optional): Maximum age of job postings in days.
    - categories (list, optional): List of job categories to filter by.
    - location (dict, optional): Dictionary with city and country to filter by.
    - location_list (list, optional): List of locations to filter by.
    - min_salary (int, optional): Minimum salary to filter by.
    - max_salary (int, optional): Maximum salary to filter by.
    - full_time (bool, optional): Filter for full-time jobs.
    - permanent (bool, optional): Filter for permanent jobs.
    - contract (bool, optional): Filter for contract jobs.
    - part_time (bool, optional): Filter for part-time jobs.
    - remote (bool, optional): Filter for remote jobs.
    - temporary (bool, optional): Filter for temporary jobs.
    - graduate (bool, optional): Filter for graduate jobs.

    Returns:
        JsonResponse: A JSON response containing aggregated job offers from the specified job providers.
    """
    results = {}

    def fetch_adzuna_jobs(params):
        job_statistics_manager.api_name = ADZUNA
        adzuna = Adzuna(job_statistics_manager)
        adzuna_job_offers = adzuna.get_jobs(country, params)
        if isinstance(adzuna_job_offers, dict):
            results[ADZUNA] = adzuna_job_offers
        else:
            LOGGER.error(
                f"Failed to fetch jobs data from Adzuna API: {adzuna_job_offers}"
            )

    def fetch_findwork_jobs(params):
        job_statistics_manager.api_name = FINDWORK
        find_work = FindWork(job_statistics_manager)
        find_work_job_offers = find_work.get_jobs(params)
        if isinstance(find_work_job_offers, dict):
            results[FINDWORK] = find_work_job_offers
        else:
            LOGGER.error(
                f"Failed to fetch jobs data from FindWork API: {find_work_job_offers}"
            )

    def fetch_reed_jobs(params):
        job_statistics_manager.api_name = REED_CO_UK
        reed_co_uk = ReedCoUk(job_statistics_manager)
        reed_co_uk_job_offers = reed_co_uk.get_jobs(params)
        if isinstance(reed_co_uk_job_offers, dict):
            results[REED_CO_UK] = reed_co_uk_job_offers
        else:
            LOGGER.error(
                f"Failed to fetch jobs data from Reed Co UK API: {reed_co_uk_job_offers}"
            )

    def fetch_the_muse_jobs(params):
        job_statistics_manager.api_name = THE_MUSE
        the_muse = TheMuse(job_statistics_manager)
        the_muse_job_offers = the_muse.get_jobs(params)
        if isinstance(the_muse_job_offers, dict):
            results[THE_MUSE] = the_muse_job_offers
        else:
            LOGGER.error(
                f"Failed to fetch jobs data from The Muse API: {the_muse_job_offers}"
            )

    parameters: dict = json.loads(request.body)

    job_title: str = parameters["job_title"]
    jobs_providers: list = parameters["jobs_providers"]
    levels: list = parameters.get("level")
    skills: list = parameters.get("skills")
    max_days_old: int = parameters.get("max_days_old")
    categories: list = parameters.get("categories")
    location: dict = parameters.get("location")
    if location:
        city: str = location.get("city")
        country: str = location.get("country")
    location_list: list = parameters.get("location_list")
    min_salary: int = parameters.get("min_salary")
    max_salary: int = parameters.get("max_salary")
    full_time: bool = parameters.get("full_time")
    permanent: bool = parameters.get("permanent")
    contract: bool = parameters.get("contract")
    part_time: bool = parameters.get("part_time")
    remote: bool = parameters.get("remote")
    temporary: bool = parameters.get("temporary")
    graduate: bool = parameters.get("graduate")

    jobs_offers = {}

    threads: list[threading.Thread] = []
    GOOGLE_DRIVE_MANAGER = GoogleDriveManager()
    job_statistics_manager = JobStatisticsManager(GOOGLE_DRIVE_MANAGER, ADZUNA)

    ####################################################
    if ADZUNA in jobs_providers:
        adzuna_params = {
            "what": job_title,
            "salary_min": min_salary,
            "salary_max": max_salary,
        }
        if max_days_old:
            adzuna_params["max_days_old"] = max_days_old
        if skills:
            adzuna_params["description"] = ",".join(skills)
        if contract:
            adzuna_params["contract"] = 1
        if full_time:
            adzuna_params["full_time"] = 1
        if permanent:
            adzuna_params["permanent"] = 1
        if part_time:
            adzuna_params["part_time"] = 1
        adzuna_thread = threading.Thread(
            target=fetch_adzuna_jobs, args=(adzuna_params,)
        )
        threads.append(adzuna_thread)

    ####################################################
    if FINDWORK in jobs_providers:
        findwork_params = {}
        if full_time:
            findwork_params["employment_type"] = "full time"
        if contract:
            findwork_params["employment_type"] = "contract"
        if part_time:
            findwork_params["employment_type"] = "contract"
        if remote:
            findwork_params["remote"] = "true"
        if location:
            if country:
                findwork_params["location"] = country
                if city:
                    findwork_params["location"] += f", {city}"
            elif city:
                findwork_params["location"] = city
        findwork_params["search"] = job_title
        findwork_thread = threading.Thread(
            target=fetch_findwork_jobs, args=(findwork_params,)
        )
        threads.append(findwork_thread)

    ####################################################
    if REED_CO_UK in jobs_providers:
        reed_params = {
            "keywords": job_title,
            "minimumSalary": min_salary,
            "maximumSalary": max_salary,
            "fullTime": full_time,
            "partTime": part_time,
            "permanent": permanent,
            "contract": contract,
            "temp": temporary,
            "graduate": graduate,
        }
        if location:
            if country:
                reed_params["locationName"] = country
                if city:
                    reed_params["locationName"] += f", {city}"
            elif city:
                reed_params["locationName"] = city
        reed_thread = threading.Thread(
            target=fetch_reed_jobs, args=(reed_params,))
        threads.append(reed_thread)

    ####################################################
    if THE_MUSE in jobs_providers:
        muse_params = {
            "query": job_title,
            "level": levels,
            "category": categories,
            "location": location_list,
        }
        muse_thread = threading.Thread(
            target=fetch_the_muse_jobs, args=(muse_params,))
        threads.append(muse_thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    jobs_offers.update(results)

    return JsonResponse({"offers": jobs_offers}, status=status.HTTP_200_OK)
