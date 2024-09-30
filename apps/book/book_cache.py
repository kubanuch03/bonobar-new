from functools import wraps
from django.core.cache import cache
from .models import Book

from rest_framework.response import Response
from rest_framework import status


CACHE_TIME = 60*15

def update_cache_on_expiry(cache_keys):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            cache_key = cache_keys
            cached_ids = cache.get(cache_key, [])

            if not cached_ids:
                print('добавляем в кеш')
                cached_ids = [obj.pk for obj in Book.objects.all()]
                cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

            return view_func(*args, **kwargs)
        
        return _wrapped_view
    return decorator

def get_object_from_cache(cache_key_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            cache_key = cache_key_func(*args, **kwargs)
            cached_instance = cache.get(cache_key)

            if cached_instance is not None:
                # Если объект найден в кеше, возвращаем его
                print(f"найден ")
                return Response(cached_instance, status=status.HTTP_200_OK)

            # Если объект не найден в кеше, вызываем метод view_func
            # для получения объекта
            cache.set(cache_key, cached_instance, timeout=CACHE_TIME)
            return view_func(*args, **kwargs)
        return _wrapped_view
    return decorator

def update_object_from_cache(cache_key_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            cache_key = cache_key_func(self, request, *args, **kwargs)
            cached_instance = cache.get(cache_key)
            if cached_instance is not None:
                return view_func(self, request, *args, **kwargs, cached_instance=cached_instance)
            return view_func(self, request, *args, **kwargs, cached_instance=None)
        return _wrapped_view
    return decorator

def get_cache_key(request, *args, **kwargs):
    instance_id = kwargs.get('pk')
    print('CACHE:', instance_id)
    return f'book_{instance_id}'
