"""
Standardized API response utilities and decorators
"""
from typing import Any, Dict, Optional, Callable
from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


class APIResponse:
    """Standardized API response wrapper"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status: int = 200) -> tuple:
        """Return success response"""
        response = {
            'success': True,
            'status': status,
            'message': message,
            'data': data
        }
        return jsonify(response), status
    
    @staticmethod
    def error(error: str, status: int = 400, details: Optional[Dict[str, Any]] = None) -> tuple:
        """Return error response"""
        response = {
            'success': False,
            'status': status,
            'error': error
        }
        if details:
            response['details'] = details
        return jsonify(response), status
    
    @staticmethod
    def paginated(data: list, page: int, per_page: int, total: int, 
                 message: str = "Success") -> tuple:
        """Return paginated response"""
        total_pages = (total + per_page - 1) // per_page
        response = {
            'success': True,
            'status': 200,
            'message': message,
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }
        return jsonify(response), 200
    
    @staticmethod
    def created(data: Any = None, message: str = "Created successfully") -> tuple:
        """Return 201 created response"""
        return APIResponse.success(data, message, 201)
    
    @staticmethod
    def no_content() -> tuple:
        """Return 204 no content response"""
        return '', 204
    
    @staticmethod
    def bad_request(error: str, details: Optional[Dict[str, Any]] = None) -> tuple:
        """Return 400 bad request response"""
        return APIResponse.error(error, 400, details)
    
    @staticmethod
    def unauthorized(error: str = "Unauthorized") -> tuple:
        """Return 401 unauthorized response"""
        return APIResponse.error(error, 401)
    
    @staticmethod
    def forbidden(error: str = "Forbidden") -> tuple:
        """Return 403 forbidden response"""
        return APIResponse.error(error, 403)
    
    @staticmethod
    def not_found(error: str = "Resource not found") -> tuple:
        """Return 404 not found response"""
        return APIResponse.error(error, 404)
    
    @staticmethod
    def conflict(error: str, details: Optional[Dict[str, Any]] = None) -> tuple:
        """Return 409 conflict response"""
        return APIResponse.error(error, 409, details)
    
    @staticmethod
    def internal_error(error: str = "Internal server error") -> tuple:
        """Return 500 internal error response"""
        return APIResponse.error(error, 500)


def json_response(func: Callable) -> Callable:
    """Decorator to standardize JSON responses"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                return result
            # Assume it's data to be wrapped in success response
            return APIResponse.success(result)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            return APIResponse.internal_error(str(e))
    return wrapper
