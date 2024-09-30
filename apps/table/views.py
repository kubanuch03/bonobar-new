from rest_framework import generics, status, response
from rest_framework.generics import get_object_or_404
from .models import Table
from .saerializers import TableListSerializer, TableCreateSerializer

from django.core.cache import cache
from django.utils.decorators import method_decorator
from .table_cache import update_cache_on_expiry, get_cache_key, get_object_from_cache
from .services import check_dublicate_table

CACHE_TIME = 60*5


@method_decorator(update_cache_on_expiry('table_ids'), name='dispatch')
class TableListApiView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableListSerializer

    def get_queryset(self):
        cache_key = 'table_ids'
        cached_ids = cache.get(cache_key, [])
        if cached_ids is None:
            return Table.objects.none()
        queryset = Table.objects.filter(pk__in=cached_ids)
        floor = self.request.query_params.get('floor', None)
        if floor:
            queryset = queryset.filter(floor__pk=floor)
        queryset = queryset.order_by('number_table')
        return queryset


class TableCreateApiView(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableCreateSerializer

    def perform_create(self, serializer):
        new_booking = serializer.validated_data
        # number_table = new_booking['number_table']
        # floor = new_booking['floor'].id
        # print(floor)
        # check_dublicate_table(floor,number_table)
        baner_instance = serializer.save()
        # Сохраняем идентификатор объекта в кеше
        cache_key = 'table_ids'
        cached_ids = cache.get(cache_key, [])
        cached_ids.append(baner_instance.pk)
        cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
        print(f"Добавлен обьект в кеш: ",cached_ids )
        

class TableDetailApiView(generics.RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableListSerializer

    @get_object_from_cache(cache_key_func=get_cache_key)
    def retrieve(self, request, *args, **kwargs):
        cached_instance = kwargs.get('table_cached_instance')
        if cached_instance is not None:
            return response.Response(cached_instance, status=status.HTTP_200_OK)
        else:
            instance = get_object_or_404(Table, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(instance)
            cache_key = get_cache_key(self, request, *args, **kwargs)
            cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
            return response.Response(serializer.data, status=status.HTTP_200_OK)


class TableUpdateApiView(generics.UpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableCreateSerializer


class TableDeleteApiView(generics.DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableListSerializer
