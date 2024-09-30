from django.core.cache import cache
from django.conf import settings
from functools import wraps
from rest_framework.response import Response

CACHE_TIMEOUT = settings.CACHE_TIME


def cache_response(cache_key, timeout=CACHE_TIMEOUT):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            else:
                response = view_func(*args, **kwargs)
                if response.status_code == 200:
                    cache.set(cache_key, response.data, timeout=timeout)
                return response
        return wrapper
    return decorator
