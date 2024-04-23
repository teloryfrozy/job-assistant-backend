"""
Handles API calls to our rest api for now
"""

from django.http import JsonResponse


def test(request):
    return JsonResponse({"message": "Test successful"})
