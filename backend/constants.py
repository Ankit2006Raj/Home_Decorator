"""
Application-wide constants and configuration values
"""
from typing import Final

# File upload constants
MAX_UPLOAD_SIZE: Final[int] = 16 * 1024 * 1024  # 16MB
ALLOWED_IMAGE_EXTENSIONS: Final[list] = ['jpg', 'jpeg', 'png', 'gif', 'webp']
ALLOWED_FILE_EXTENSIONS: Final[list] = ['pdf', 'txt', 'json', 'csv']

# API constants
DEFAULT_PAGE_SIZE: Final[int] = 20
MAX_PAGE_SIZE: Final[int] = 100
API_VERSION: Final[str] = 'v1'
API_TIMEOUT: Final[int] = 30  # Timeout in seconds for API calls

# Room dimension constants
MIN_ROOM_LENGTH: Final[float] = 2.0
MAX_ROOM_LENGTH: Final[float] = 100.0
MIN_ROOM_WIDTH: Final[float] = 2.0
MAX_ROOM_WIDTH: Final[float] = 100.0
MIN_ROOM_HEIGHT: Final[float] = 2.4
MAX_ROOM_HEIGHT: Final[float] = 10.0

# Furniture constants
MAX_FURNITURE_ITEMS: Final[int] = 500
DEFAULT_FURNITURE_SCALE: Final[float] = 1.0
MIN_FURNITURE_SCALE: Final[float] = 0.1
MAX_FURNITURE_SCALE: Final[float] = 5.0

# AI service constants
GEMINI_MODEL_NAME: Final[str] = 'gemini-pro'
AI_TIMEOUT: Final[int] = 60

# Database constants
DB_POOL_SIZE: Final[int] = 10
DB_MAX_OVERFLOW: Final[int] = 20

# Cache constants
CACHE_TIMEOUT: Final[int] = 3600
CACHE_DEFAULT_TIMEOUT: Final[int] = 300

# Error messages
ERROR_INVALID_INPUT: Final[str] = 'Invalid input provided'
ERROR_RESOURCE_NOT_FOUND: Final[str] = 'Resource not found'
ERROR_UNAUTHORIZED: Final[str] = 'Unauthorized access'
ERROR_INTERNAL_SERVER: Final[str] = 'Internal server error'
