"""
TODO: clean doc
Our RestAPi endpoints
"""

from django.urls import path

from core.scheduled_tasks import adzuna_run
from . import views

app_name = "job_assistant"

urlpatterns = [
    path("adzuna_run/", adzuna_run(), name="adzuna_run")
    ]
