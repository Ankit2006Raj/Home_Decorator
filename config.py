import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class with common settings."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///home_decorator.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    UPLOADS_FOLDER = 'frontend/assets/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

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
