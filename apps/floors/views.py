from django.shortcuts import render
from .models import Floor
from .serializers import FloorSerializer
from .cache_floors import update_cache_on_expiry,update_object_from_cache, get_cache_key, get_object_from_cache
from rest_framework import generics,status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator



CACHE_TIME = 60*5

class FloorCreateApiView(generics.CreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def perform_create(self, serializer):
        baner_instance = serializer.save()
        # Сохраняем идентификатор объекта в кеше
        cache_key = 'floor_ids'
        cached_ids = cache.get(cache_key, [])
        cached_ids.append(baner_instance.pk)
        cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
        print(f"Добавлен обьект в кеш: ",cached_ids )


# @method_decorator(update_cache_on_expiry('floor_ids'), name='dispatch')
class FloorListApiView(generics.ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    # def get_queryset(self):
    #     cache_key = 'floor_ids'
    #     cached_ids = cache.get(cache_key, [])
    #     print(cached_ids)
    #     return Floor.objects.filter(pk__in=cached_ids)


class FloorDetailApiView(generics.RetrieveAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    @get_object_from_cache(cache_key_func=get_cache_key)
    def retrieve(self, request, *args, **kwargs):
        cached_instance = kwargs.get('floor_cached_instance')
        if cached_instance is not None:
            return Response(cached_instance, status=status.HTTP_200_OK)
        else:
            instance = get_object_or_404(Floor, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(instance)
            cache_key = get_cache_key(self, request, *args, **kwargs)
            cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
            return Response(serializer.data, status=status.HTTP_200_OK)

class FloorUpdateApiView(generics.UpdateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class FloorDeleteApiView(generics.DestroyAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    # @get_object_from_cache(cache_key_func=get_cache_key)
    def delete(self, request, *args, **kwargs):
        cached_instance = kwargs.get('floor_cached_instance')
        instance = self.get_object() if cached_instance is None else cached_instance

        # Удаляем объект из базы данных
        instance.delete()

        # Удаляем объект из кеша
        cache_key = get_cache_key(self, request, *args, **kwargs)
        cache.delete(cache_key)

        # Возвращаем успешный ответ
        return Response({"delete":"удалено!"},status=status.HTTP_204_NO_CONTENT)

#не правильно работет кеш вссе эндпойнты не обновляют кеш