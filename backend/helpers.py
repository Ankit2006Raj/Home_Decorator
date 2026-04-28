"""
General purpose helper utilities for common operations

This module provides utility classes for datetime handling, hashing, UUID generation,
and other common operations used throughout the application.
"""
import hashlib
import uuid
import json
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)


class DateTimeUtils:
    """DateTime utility functions for handling time operations across the application"""
    
    @staticmethod
    def now_utc() -> datetime:
        """Get current UTC datetime in ISO format"""
        return datetime.utcnow()
    
    @staticmethod
    def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Format datetime object to string representation"""
        return dt.strftime(fmt)
    
    @staticmethod
    def get_timestamp() -> int:
        """Get current Unix timestamp in seconds since epoch"""
        return int(datetime.utcnow().timestamp())
    
    @staticmethod
    def parse_datetime(date_string: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime:
        """Parse string to datetime"""
        return datetime.strptime(date_string, fmt)
    
    @staticmethod
    def days_ago(days: int) -> datetime:
        """Get datetime from N days ago"""
        return datetime.utcnow() - timedelta(days=days)
    
    @staticmethod
    def hours_ago(hours: int) -> datetime:
        """Get datetime from N hours ago"""
        return datetime.utcnow() - timedelta(hours=hours)


class StringUtils:
    """String utility functions"""
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate a unique UUID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a random token"""
        return hashlib.sha256(os.urandom(32)).hexdigest()[:length]
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Generate a hash of password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hash_val: str) -> bool:
        """Verify password against hash"""
        return hashlib.sha256(password.encode()).hexdigest() == hash_val
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        text = text.lower()
        text = re.sub(r'[\\s]+', '-', text)  # Replace spaces with hyphens
        text = re.sub(r'[^\\w\\-]', '', text)  # Remove non-alphanumeric chars
        text = re.sub(r'\\-+', '-', text)  # Replace multiple hyphens
        return text.strip('-')
    
    @staticmethod
    def truncate(text: str, length: int = 100, suffix: str = '...') -> str:
        """Truncate text to specified length"""
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix


class FileUtils:
    """File utility functions"""
    
    @staticmethod
    def ensure_directory(path: str):
        """Ensure directory exists"""
        os.makedirs(path, exist_ok=True)
        logger.info(f"Ensured directory exists: {path}")
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension"""
        return os.path.splitext(file_path)[1].lstrip('.')
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """Read JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any], pretty: bool = True):
        """Write data to JSON file"""
        try:
            FileUtils.ensure_directory(os.path.dirname(file_path))
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2 if pretty else None)
            logger.info(f"Wrote JSON file: {file_path}")
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {str(e)}")
            raise


class CollectionUtils:
    """Collection utility functions"""
    
    @staticmethod
    def flatten(nested_list: list) -> list:
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(CollectionUtils.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def chunk(items: list, chunk_size: int) -> list:
        """Split list into chunks"""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    
    @staticmethod
    def deduplicate(items: list) -> list:
        """Remove duplicates from list maintaining order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def merge_dicts(*dicts: Dict) -> Dict:
        """Merge multiple dictionaries"""
        result = {}
        for d in dicts:
            result.update(d)
        return result
# Update
