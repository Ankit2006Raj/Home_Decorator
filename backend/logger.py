"""
Centralized logging configuration and utilities for application debugging and monitoring
"""
import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class LoggerSetup:
    """Setup and configuration for application logging"""
    
    _loggers = {}
    
    @staticmethod
    def setup_logger(name: str, log_level: str = "INFO", 
                    log_file: Optional[str] = None) -> logging.Logger:
        """Setup a logger with console and optional file handlers"""
        
        if name in LoggerSetup._loggers:
            return LoggerSetup._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        LoggerSetup._loggers[name] = logger
        return logger
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get an existing logger or create a new one"""
        if name not in LoggerSetup._loggers:
            return LoggerSetup.setup_logger(name)
        return LoggerSetup._loggers[name]


class PerformanceLogger:
    """Utility class for performance logging"""
    
    @staticmethod
    def log_execution_time(func_name: str, execution_time: float, 
                          logger: logging.Logger, threshold: float = 1.0):
        """Log function execution time if it exceeds threshold"""
        if execution_time > threshold:
            logger.warning(
                f"Slow execution: {func_name} took {execution_time:.2f}s (threshold: {threshold}s)"
            )
        else:
            logger.debug(f"{func_name} executed in {execution_time:.2f}s")
