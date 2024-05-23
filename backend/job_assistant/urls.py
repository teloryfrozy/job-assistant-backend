"""
This file sets up the URLs for the job_assistant app.
Each URL connects to a function in views to handle requests.
"""

from django.urls import path
from . import views

app_name = "job_assistant"

urlpatterns = [
    path("test/", views.test, name="test"),
    path("api/get_jobs", views.get_jobs, name="get_jobs"),
    path("api/get_jobs_arbeit_now", views.get_jobs_arbeit_now, name="get_jobs_arbeit_now")
]
