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
from django.db import IntegrityError, DatabaseError
from .utils import api_response

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Wrap all DRF errors in your api_response envelope:
    { "success": False, "message": "...", "data": { ... } }
    """
    CONSTRAINT_MESSAGES = {
        "users_one_role_ck": "A user cannot be both tenant and manager at the same time.",
        "uniq_active_user_email": "Email already exists for an active user.",
    }
    if isinstance(exc, (IntegrityError, DatabaseError)):

        
        msg = str(exc).replace("\n", " ").lower()

        # # Try to find a matching constraint 
        for constraint, message in CONSTRAINT_MESSAGES.items():
            if constraint in msg:
                return api_response(False, message, None, drf_status.HTTP_400_BAD_REQUEST,
                )
        return api_response(
           False, "Database integrity error.", None,drf_status.HTTP_400_BAD_REQUEST)
         

    # Let DRF build the base response first
    response = exception_handler(exc, context)

    # If DRF didn't handle it (uncaught error), make a generic 500
    if response is None:
        # Log full traceback to server console/logs
        logger.exception("Unhandled exception in API view", exc_info=exc)

        # In DEBUG, surface a brief error; otherwise generic
        message = str(exc) if getattr(settings, "DEBUG", False) else "Server error"
        return api_response(
            False, message, None, drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    # Decide a friendly message by exception type
    if isinstance(exc, ValidationError):
        message = "Validation error"
        flat_data = {}
        if isinstance(response.data, dict):
            for field, errors in response.data.items():
                if isinstance(errors, list) and errors:
                    flat_data[field] = errors[0]  # take first error
                else:
                    flat_data[field] = errors
            response.data = flat_data
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
    return api_response(False,message, response.data,response.status_code)
