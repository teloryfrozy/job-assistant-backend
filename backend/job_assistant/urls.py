"""
TODO: clean doc
Our RestAPi endpoints
"""

from django.urls import path

from . import views

app_name = "job_assistant"

urlpatterns = [path("test/", views.test, name="test")]
