from functools import wraps
from django.core.cache import cache
from .models import BanerMain,BanerMainTopik

from rest_framework.response import Response
from rest_framework import status


CACHE_TIME = 20

def update_cache_on_expiry(cache_keys):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Проверяем кеш
            cache_key = cache_keys
            cached_ids = cache.get(cache_key, [])

            # Если кеш пустой, обновляем его
            if not cached_ids:
                # Ваш код для обновления кеша
                print('добавляем в кеш')
                cached_ids = [obj.pk for obj in BanerMain.objects.all()]
                cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

            # Вызываем представление
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
    return f'baner_{instance_id}'


# #== Baner Middle =====================================================================================================================================================


def topik_update_cache_on_expiry(cache_keys):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Проверяем кеш
            cache_key = cache_keys
            cached_ids = cache.get(cache_key, [])

            # Если кеш пустой, обновляем его
            if not cached_ids:
                # Ваш код для обновления кеша
                print('добавляем в кеш')
                cached_ids = [obj.pk for obj in BanerMainTopik.objects.all()]
                cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

            # Вызываем представление
            return view_func(*args, **kwargs)
        
        return _wrapped_view
    return decorator

def topik_get_object_from_cache(cache_key_func):
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

def topik_update_object_from_cache(cache_key_func):
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

def topik_get_cache_key(request, *args, **kwargs):
    instance_id = kwargs.get('pk')
    print('CACHE:', instance_id)
    return f'baner_topik_{instance_id}'
# #== Baner Middle =====================================================================================================================================================
# def baner_middle_update_cache_on_expiry(cache_key):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(*args, **kwargs):
#             # Проверяем кеш
#             # cache_key = cache_keys
#             cached_ids = cache.get(cache_key, [])

#             # Если кеш пустой, обновляем его
#             if not cached_ids:
#                 # Ваш код для обновления кеша
#                 print('добавляем в кеш')
#                 cached_ids = [obj.pk for obj in BanerMiddle.objects.all()]
#                 cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

#             # Вызываем представление
#             return view_func(*args, **kwargs)
        
#         return _wrapped_view
#     return decorator

# def baner_middle_get_object_from_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(*args, **kwargs):
#             cache_key = cache_key_func(*args, **kwargs)
#             cached_instance = cache.get(cache_key)

#             if cached_instance is not None:
#                 # Если объект найден в кеше, возвращаем его
#                 print(f"найден в кеше: {cache_key}")
#                 return Response(cached_instance, status=status.HTTP_200_OK)

#             # Если объект не найден в кеше, вызываем метод view_func
#             return view_func(*args, **kwargs)
#         return _wrapped_view
#     return decorator

# def baner_middle_update_object_from_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(self, request, *args, **kwargs):
#             cache_key = cache_key_func(self, request, *args, **kwargs)
#             cached_instance = cache.get(cache_key)
#             if cached_instance is not None:
#                 return view_func(self, request, *args, **kwargs, cached_instance=cached_instance)
#             return view_func(self, request, *args, **kwargs, cached_instance=None)
#         return _wrapped_view
#     return decorator


# def baner_middle_update_object_in_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(self, request, *args, **kwargs):
#             response = view_func(self, request, *args, **kwargs)

#             if response.status_code == status.HTTP_200_OK:
#                 cache_key = cache_key_func(self, request, *args, **kwargs)
#                 cache.set(cache_key, response.data, timeout=CACHE_TIME)

#             return response
#         return _wrapped_view
#     return decorator

# def baner_middle_get_cache_key(request, *args, **kwargs):
#     instance_id = kwargs.get('pk')
#     cache_key = f'baner_middle_{instance_id}'
#     print(f'Генерация кеш ключа: {cache_key}')  # Добавьте отладочную информацию
#     return cache_key

# #== Baner Book ======================================================================================================================================================
# def baner_book_update_cache_on_expiry(cache_key):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(*args, **kwargs):
#             # Проверяем кеш
#             # cache_key = cache_keys
#             cached_ids = cache.get(cache_key, [])

#             # Если кеш пустой, обновляем его
#             if not cached_ids:
#                 # Ваш код для обновления кеша
#                 print('добавляем в кеш')
#                 cached_ids = [obj.pk for obj in BanerBook.objects.all()]
#                 cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

#             # Вызываем представление
#             return view_func(*args, **kwargs)
        
#         return _wrapped_view
#     return decorator


# def baner_book_get_object_from_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(*args, **kwargs):
#             cache_key = cache_key_func(*args, **kwargs)
#             cached_instance = cache.get(cache_key)

#             if cached_instance is not None:
#                 # Если объект найден в кеше, возвращаем его
#                 print(f"найден ")
#                 return Response(cached_instance, status=status.HTTP_200_OK)

#             # Если объект не найден в кеше, вызываем метод view_func
#             # для получения объекта
#             cache.set(cache_key, cached_instance, timeout=CACHE_TIME)
#             return view_func(*args, **kwargs)
#         return _wrapped_view
#     return decorator

# def baner_book_update_object_from_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(self, request, *args, **kwargs):
#             cache_key = cache_key_func(self, request, *args, **kwargs)
#             cached_instance = cache.get(cache_key)
#             if cached_instance is not None:
#                 return view_func(self, request, *args, **kwargs, cached_instance=cached_instance)
#             return view_func(self, request, *args, **kwargs, cached_instance=None)
#         return _wrapped_view
#     return decorator


# def baner_book_update_object_in_cache(cache_key_func):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(self, request, *args, **kwargs):
#             response = view_func(self, request, *args, **kwargs)

#             if response.status_code == status.HTTP_200_OK:
#                 cache_key = cache_key_func(self, request, *args, **kwargs)
#                 cache.set(cache_key, response.data, timeout=CACHE_TIME)

#             return response
#         return _wrapped_view
#     return decorator

# def baner_book_get_cache_key(request, *args, **kwargs):
#     instance_id = kwargs.get('pk')
#     print('CACHE:', instance_id)
#     return f'baner_book_{instance_id}'
