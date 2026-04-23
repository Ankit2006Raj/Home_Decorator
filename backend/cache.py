"""
Caching utilities and decorators
"""
import time
import logging
from functools import wraps
from typing import Optional, Callable, Any, Dict

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache implementation"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if entry['expires'] > time.time():
                logger.debug(f"Cache hit: {key}")
                return entry['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }
        logger.debug(f"Cache set: {key} (ttl: {ttl}s)")
    
    def delete(self, key: str):
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache delete: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [k for k, v in self.cache.items() if v['expires'] <= current_time]
        for key in expired_keys:
            del self.cache[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global cache instance
_cache = SimpleCache()


def cache_result(ttl: int = 300):
    """Decorator to cache function results"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = _cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator


def get_cache():
    """Get global cache instance"""
    return _cache
