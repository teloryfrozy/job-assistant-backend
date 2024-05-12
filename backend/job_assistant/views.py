"""
Handles API calls to our rest api for now
"""

import logging
from django.http import JsonResponse
from django.contrib.auth.models import User


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)



def test(request):
    return JsonResponse({"message": "Test successful"})
