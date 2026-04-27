"""
Centralized error handling and custom exceptions

This module provides a hierarchy of custom exception classes for the API,
allowing for standardized error responses and proper HTTP status codes.
"""
import logging
from typing import Dict, Any, Optional
from flask import jsonify

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message: str, status_code: int = 500, payload: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary response"""
        rv = dict(self.payload)
        rv['message'] = self.message
        rv['error'] = self.__class__.__name__
        rv['status'] = self.status_code
        return rv


class ValidationError(APIException):
    """Raised when validation fails"""
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, payload)


class NotFoundError(APIException):
    """Raised when resource is not found"""
    def __init__(self, message: str = "Resource not found", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, payload)


class UnauthorizedError(APIException):
    """Raised when user is not authorized"""
    def __init__(self, message: str = "Unauthorized access", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 401, payload)


class ForbiddenError(APIException):
    """Raised when user doesn't have permission"""
    def __init__(self, message: str = "Forbidden", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, payload)


class DatabaseError(APIException):
    """Raised when database operation fails"""
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 500, payload)


class ServiceError(APIException):
    """Raised when external service fails"""
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 503, payload)


def handle_api_exception(error: APIException):
    """Handle API exceptions and return proper response"""
    logger.error(f"{error.__class__.__name__}: {error.message}")
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def safe_call(func, *args, error_message: str = "Operation failed", **kwargs):
    """Safely call a function with error handling"""
    try:
        return func(*args, **kwargs)
    except APIException:
        raise
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}", exc_info=True)
        raise ServiceError(error_message)
