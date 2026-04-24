"""Application Configuration Module

Handles all environment-based configuration and settings for the Home Decorator application.
Supports development, testing, and production environments.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Base configuration class with common settings with enhanced validation."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///home_decorator.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    UPLOADS_FOLDER = 'frontend/assets/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Enhanced settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PREFERRED_URL_SCHEME = 'https'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    @classmethod
    def validate_config(cls):
        """Validate configuration on startup"""
        if not os.path.exists(os.path.dirname(cls.UPLOADS_FOLDER)):
            os.makedirs(os.path.dirname(cls.UPLOADS_FOLDER), exist_ok=True)
            logger.info(f"Created uploads folder: {cls.UPLOADS_FOLDER}")
        
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            logger.warning("Using default SECRET_KEY - change this in production!")
        
        logger.info(f"Using database: {cls.SQLALCHEMY_DATABASE_URI}")

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = False

class TestingConfig(Config):
    """Testing environment configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
