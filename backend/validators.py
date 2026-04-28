"""
Input validation utilities and sanitization functions
"""
import re
from typing import Any, Optional, List, Dict
from backend.errors import ValidationError


class Validator:
    """Input validation utility class for form data and API parameters"""
    
    @staticmethod
    def validate_string(value: Any, field_name: str, min_length: int = 1, 
                       max_length: int = 255, allow_empty: bool = False) -> str:
        """Validate and sanitize string input values with length constraints"""
        if value is None:
            if allow_empty:
                return ""
            raise ValidationError(f"{field_name} cannot be empty")
        
        value_str = str(value).strip()
        
        if not allow_empty and not value_str:
            raise ValidationError(f"{field_name} cannot be empty")
        
        if len(value_str) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters")
        
        if len(value_str) > max_length:
            raise ValidationError(f"{field_name} must not exceed {max_length} characters")
        
        return value_str
    
    @staticmethod
    def validate_number(value: Any, field_name: str, min_val: Optional[float] = None,
                       max_val: Optional[float] = None, is_integer: bool = False) -> float:
        """Validate and return numeric value"""
        try:
            if is_integer:
                num = int(value)
            else:
                num = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid number")
        
        if min_val is not None and num < min_val:
            raise ValidationError(f"{field_name} must be at least {min_val}")
        
        if max_val is not None and num > max_val:
            raise ValidationError(f"{field_name} must not exceed {max_val}")
        
        return num
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email address"""
        email = email.strip()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValidationError("Invalid email address")
        
        return email
    
    @staticmethod
    def validate_url(url: str) -> str:
        """Validate URL"""
        url = url.strip()
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        
        if not re.match(pattern, url, re.IGNORECASE):
            raise ValidationError("Invalid URL format")
        
        return url
    
    @staticmethod
    def validate_choice(value: Any, field_name: str, choices: List[str]) -> str:
        """Validate that value is one of allowed choices"""
        value_str = str(value).strip().lower()
        choices_lower = [c.lower() for c in choices]
        
        if value_str not in choices_lower:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(choices)}"
            )
        
        return value_str
    
    @staticmethod
    def validate_array(value: Any, field_name: str, min_items: int = 0,
                      max_items: Optional[int] = None) -> list:
        """Validate array/list input"""
        if not isinstance(value, list):
            raise ValidationError(f"{field_name} must be an array")
        
        if len(value) < min_items:
            raise ValidationError(f"{field_name} must have at least {min_items} items")
        
        if max_items is not None and len(value) > max_items:
            raise ValidationError(f"{field_name} must not exceed {max_items} items")
        
        return value
    
    @staticmethod
    def validate_dict(value: Any, field_name: str, required_keys: Optional[List[str]] = None) -> dict:
        """Validate dictionary input"""
        if not isinstance(value, dict):
            raise ValidationError(f"{field_name} must be a dictionary")
        
        if required_keys:
            missing_keys = set(required_keys) - set(value.keys())
            if missing_keys:
                raise ValidationError(
                    f"{field_name} missing required fields: {', '.join(missing_keys)}"
                )
        
        return value
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Sanitize string by removing dangerous characters"""
        value = str(value).strip()
        # Remove script tags and suspicious patterns
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
        value = value[:max_length]
        return value
