"""
Useful decorators for Flask applications
"""
import logging
import time
from functools import wraps
from typing import Callable
from flask import request, jsonify

logger = logging.getLogger(__name__)


def measure_time(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 1.0:
            logger.warning(f"{func.__name__} took {execution_time:.2f}s to execute")
        else:
            logger.debug(f"{func.__name__} executed in {execution_time:.2f}s")
        
        return result
    return wrapper


def require_json(func: Callable) -> Callable:
    """Decorator to require JSON content type"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return func(*args, **kwargs)
    return wrapper


def handle_errors(func: Callable) -> Callable:
    """Decorator to handle common errors in routes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except KeyError as e:
            logger.error(f"Missing key in {func.__name__}: {str(e)}")
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper


def rate_limit(calls: int = 100, period: int = 60):
    """Decorator for rate limiting"""
    def decorator(func: Callable) -> Callable:
        request_times = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            client_id = request.remote_addr
            
            if client_id not in request_times:
                request_times[client_id] = []
            
            # Remove old requests outside the period
            request_times[client_id] = [
                req_time for req_time in request_times[client_id]
                if now - req_time < period
            ]
            
            # Check rate limit
            if len(request_times[client_id]) >= calls:
                logger.warning(f"Rate limit exceeded for {client_id}")
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            request_times[client_id].append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def log_request(func: Callable) -> Callable:
    """Decorator to log request details"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Request: {request.method} {request.path}")
        logger.debug(f"Headers: {dict(request.headers)}")
        if request.is_json:
            logger.debug(f"JSON Data: {request.get_json()}")
        
        result = func(*args, **kwargs)
        
        if isinstance(result, tuple):
            status_code = result[1] if len(result) > 1 else 200
        else:
            status_code = 200
        
        logger.info(f"Response: {status_code}")
        return result
    
    return wrapper
