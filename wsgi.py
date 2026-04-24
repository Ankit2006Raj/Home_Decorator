"""
WSGI entry point for production deployment with enhanced error handling.

This module serves as the application interface for production servers like Gunicorn.
Implements proper logging and error handling for graceful failure recovery.
"""
import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    logger.info(f"Application created successfully for {os.getenv('FLASK_ENV', 'production')} environment")
except Exception as e:
    logger.error(f"Failed to create application: {str(e)}", exc_info=True)
    raise

if __name__ == "__main__":
    app.run()
