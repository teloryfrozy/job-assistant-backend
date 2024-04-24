"""
Handles API calls to our rest api for now
"""

from django.http import JsonResponse
from django.contrib.auth.models import User


def test(request):
    return JsonResponse({"message": "Test successful"})
