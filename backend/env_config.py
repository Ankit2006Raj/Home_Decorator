"""
Environment variable validation and configuration utilities
"""
import os
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class EnvironmentValidator:
    """Validate and manage environment variables"""
    
    @staticmethod
    def get_required(key: str, error_message: Optional[str] = None) -> str:
        """Get required environment variable"""
        value = os.getenv(key)
        if not value:
            msg = error_message or f"Required environment variable '{key}' is not set"
            logger.error(msg)
            raise ValueError(msg)
        return value
    
    @staticmethod
    def get_optional(key: str, default: Optional[Any] = None) -> Any:
        """Get optional environment variable"""
        return os.getenv(key, default)
    
    @staticmethod
    def get_int(key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
        """Get environment variable as integer"""
        value = os.getenv(key)
        if not value:
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default
        
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Environment variable '{key}' must be a valid integer, got: {value}")
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """Get environment variable as boolean"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_float(key: str, default: Optional[float] = None, required: bool = False) -> Optional[float]:
        """Get environment variable as float"""
        value = os.getenv(key)
        if not value:
            if required:
                raise ValueError(f"Required environment variable '{key}' is not set")
            return default
        
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Environment variable '{key}' must be a valid float, got: {value}")
    
    @staticmethod
    def validate_all(required_vars: List[str]) -> Dict[str, str]:
        """Validate multiple required environment variables"""
        missing = []
        values = {}
        
        for key in required_vars:
            value = os.getenv(key)
            if not value:
                missing.append(key)
            else:
                values[key] = value
        
        if missing:
            msg = f"Missing required environment variables: {', '.join(missing)}"
            logger.error(msg)
            raise ValueError(msg)
        
        return values
    
    @staticmethod
    def log_environment(keys: List[str], mask_sensitive: bool = True):
        """Log environment variables for debugging"""
        sensitive_keys = {'API_KEY', 'SECRET', 'PASSWORD', 'TOKEN', 'CREDENTIAL'}
        
        logger.info("Environment Configuration:")
        for key in keys:
            value = os.getenv(key)
            if mask_sensitive and any(sensitive in key.upper() for sensitive in sensitive_keys):
                display_value = "***" if value else "NOT SET"
            else:
                display_value = value or "NOT SET"
            logger.info(f"  {key}: {display_value}")


class ConfigValidator:
    """Validate application configuration"""
    
    @staticmethod
    def validate_database_url(db_url: str) -> bool:
        """Validate database URL format"""
        valid_prefixes = ('sqlite://', 'postgresql://', 'mysql://', 'oracle://')
        return any(db_url.startswith(prefix) for prefix in valid_prefixes)
    
    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number"""
        return 1 <= port <= 65535
    
    @staticmethod
    def validate_log_level(level: str) -> bool:
        """Validate log level"""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        return level.upper() in valid_levels
