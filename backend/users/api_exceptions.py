# users/api_exceptions.py
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
    Throttled,
)
from django.conf import settings

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Wrap all DRF errors in your api_response envelope:
    { "success": False, "message": "...", "data": { ... } }
    """
    # Let DRF build the base response first
    response = exception_handler(exc, context)

    # If DRF didn't handle it (uncaught error), make a generic 500
    if response is None:
        # Log full traceback to server console/logs
        logger.exception("Unhandled exception in API view", exc_info=exc)

        # In DEBUG, surface a brief error; otherwise generic
        message = str(exc) if getattr(settings, "DEBUG", False) else "Server error"
        return Response(
            {"success": False, "message": message, "data": None},
            status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    # Decide a friendly message by exception type
    if isinstance(exc, ValidationError):
        message = "Validation error"
    elif isinstance(exc, NotAuthenticated):
        message = "Authentication credentials were not provided."
    elif isinstance(exc, AuthenticationFailed):
        message = "Invalid authentication credentials."
    elif isinstance(exc, PermissionDenied):
        message = "You do not have permission to perform this action."
    elif isinstance(exc, NotFound):
        message = "Resource not found"
    elif isinstance(exc, Throttled):
        # DRF already sets detail like "Request was throttled. Expected available in X seconds."
        message = "Request was throttled. Try again later."
    else:
        # Fallback: use DRF's detail if present, else generic
        detail = None
        if isinstance(response.data, dict):
            detail = response.data.get("detail")
        message = detail or "Error"

    # Wrap original response.data into your envelope
    return Response(
        {"success": False, "message": message, "data": response.data},
        status=response.status_code,
    )
