from functools import wraps
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

CACHE_TIME = settings.CACHE_TIME


def cache_get_response(cache_key_func, timeout=CACHE_TIME):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            cache_key = cache_key_func(self, request, *args, **kwargs)
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            response = view_func(self, request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                cache.set(cache_key, response.data, timeout=timeout)

            return response
        return _wrapped_view
    return decorator


def get_object_from_cache(cache_key_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            cache_key = cache_key_func(*args, **kwargs)
            cached_instance = cache.get(cache_key)

            if cached_instance is not None:
                return Response(cached_instance, status=status.HTTP_200_OK)

            response = view_func(*args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                cache.set(cache_key, response.data, timeout=CACHE_TIME)
            return view_func(*args, **kwargs)
        return _wrapped_view
    return decorator


def delete_object_from_cache(cache_key_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            response = view_func(*args, **kwargs)
            cache_key = cache_key_func(*args, **kwargs)
            cache.delete(cache_key)
            return response
        return _wrapped_view
    return decorator


def get_cache_key(request, *args, **kwargs):
    instance_id = kwargs.get('pk')
    print('CACHE:', instance_id)
    return f'sub_category_{instance_id}'
