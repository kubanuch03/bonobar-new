from rest_framework import generics, permissions, status
from rest_framework. response import Response
from rest_framework.generics import get_object_or_404
from .models import BanerMain, BanerMiddle, BanerBook, BanerMainTopik
from .serializers import *
from .cache_baner import *
from django.core.cache import cache
from django.utils.decorators import method_decorator

CACHE_TIME = 60*5




#==  Baner Main =============================================================================
class BanerMainCreateApiView(generics.CreateAPIView):
    # queryset = Baner.objects.all()
    serializer_class = BanerCreateSerializers

    def perform_create(self, serializer):
        baner_instance = serializer.save()
        # Сохраняем идентификатор объекта в кеше
        cache_key = 'baner_ids'
        cached_ids = cache.get(cache_key, [])
        cached_ids.append(baner_instance.pk)
        cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
        print(f"Добавлен обьект в кеш: ",cached_ids )







@method_decorator(update_cache_on_expiry('baner_ids'), name='dispatch')
class BanerMainListApiView(generics.ListAPIView):
    # queryset = Baner.objects.all()
    serializer_class = BanerListSerializers

    def get_queryset(self):
        cache_key = 'baner_ids'
        cached_ids = cache.get(cache_key, [])
        print(cached_ids)
        return BanerMain.objects.filter(pk__in=cached_ids)


class BanerMainDetailApiView(generics.RetrieveAPIView):
    queryset = BanerMain.objects.all()
    serializer_class = BanerListSerializers

    @get_object_from_cache(cache_key_func=get_cache_key)
    def retrieve(self, request, *args, **kwargs):
        cached_instance = kwargs.get('cached_instance')
        if cached_instance is not None:
            return Response(cached_instance, status=status.HTTP_200_OK)
        else:
            instance = get_object_or_404(BanerMain, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(instance)
            cache_key = get_cache_key(self, request, *args, **kwargs)
            cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
            return Response(serializer.data, status=status.HTTP_200_OK)





class BanerMainUpdateApiView(generics.UpdateAPIView):
    queryset = BanerMain.objects.all()
    serializer_class = BanerUpdateSerializers

    # @get_object_from_cache(cache_key_func=get_cache_key)
    # def perform_update(self, serializer, *args, **kwargs):
    #     cached_instance = kwargs.get('cached_instance')
    #     instance = self.get_object() if cached_instance is None else cached_instance

    #     # Обновляем данные в базе данных
    #     super().perform_update(serializer)

    #     # Обновляем данные в кеше
    #     cache_key = get_cache_key(self, self.request, *args, **kwargs)
    #     cache.set(cache_key, serializer.data, timeout=CACHE_TIME)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    

class BanerMainDeleteApiView(generics.DestroyAPIView):
    queryset = BanerMain.objects.all()
    serializer_class = BanerCreateSerializers

    @get_object_from_cache(cache_key_func=get_cache_key)
    def delete(self, request, *args, **kwargs):
        cached_instance = kwargs.get('cached_instance')
        instance = self.get_object() if cached_instance is None else cached_instance

        # Удаляем объект из базы данных
        instance.delete()

        # Удаляем объект из кеша
        cache_key = get_cache_key(self, request, *args, **kwargs)
        cache.delete(cache_key)

        # Возвращаем успешный ответ
        return Response({"delete":"удалено!"},status=status.HTTP_204_NO_CONTENT)


#==  Baner Main Topik =============================================================================

@method_decorator(topik_update_cache_on_expiry('baner_topik_ids'), name='dispatch')
class BanerMainTopikListApiView(generics.ListAPIView):
    # queryset = BanerMainTopik.objects.all()
    serializer_class = BanerTopikCreateSerializers


    def get_queryset(self):
        cache_key = 'baner_topik_ids'
        cached_ids = cache.get(cache_key, [])
        print(cached_ids)
        return BanerMainTopik.objects.filter(pk__in=cached_ids)


class BanerMainTopikDetailApiView(generics.RetrieveAPIView):
    queryset = BanerMainTopik.objects.all()
    serializer_class = BanerTopikCreateSerializers

    @topik_get_object_from_cache(cache_key_func=topik_get_cache_key)
    def retrieve(self, request, *args, **kwargs):
        cached_instance = kwargs.get('baner_topik_cached_instance')
        if cached_instance is not None:
            return Response(cached_instance, status=status.HTTP_200_OK)
        else:
            instance = get_object_or_404(BanerMainTopik, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(instance)
            cache_key = topik_get_cache_key(self, request, *args, **kwargs)
            cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
            return Response(serializer.data, status=status.HTTP_200_OK)

class BanerMainTopikCreateApiView(generics.CreateAPIView):
    # queryset = BanerMainTopik.objects.all()
    serializer_class = BanerTopikCreateSerializers

    def perform_create(self, serializer):
        baner_instance = serializer.save()
        # Сохраняем идентификатор объекта в кеше
        cache_key = 'baner_topik_ids'
        cached_ids = cache.get(cache_key, [])
        cached_ids.append(baner_instance.pk)
        cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
        print(f"Добавлен обьект в кеш: ",cached_ids )

class BanerMainTopikUpdateApiView(generics.UpdateAPIView):
    queryset = BanerMainTopik.objects.all()
    serializer_class = BanerTopikUpdateSerializers

class BanerMainTopikDeleteApiView(generics.DestroyAPIView):
    queryset = BanerMainTopik.objects.all()
    serializer_class = BanerTopikUpdateSerializers



#==  Baner Middle ==================================================================================================================================================

# class BanerMiddleCreateApiView(generics.CreateAPIView):
#     # queryset = BanerVideo.objects.all()
#     serializer_class = BanerMiddleSerializers

#     def perform_create(self, serializer):
#         baner_instance = serializer.save()
#         # Сохраняем идентификатор объекта в кеше
#         cache_key = 'baner_middle_ids'
#         cached_ids = cache.get(cache_key, [])
#         cached_ids.append(baner_instance.pk)
#         cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
#         print(f"Добавлен обьект в кеш: ",cached_ids )


# @method_decorator(baner_middle_update_cache_on_expiry('baner_middle_ids'), name='dispatch')
# class BanerMiddleListApiView(generics.ListAPIView):
#     # queryset = BanerVideo.objects.all()
#     serializer_class = BanerMiddleSerializers

#     def get_queryset(self):
#         cache_key = 'baner_middle_ids'
#         cached_ids = cache.get(cache_key, [])
#         print(cached_ids)
#         return BanerMiddle.objects.filter(pk__in=cached_ids)


# class BanerMiddleDetailApiView(generics.RetrieveAPIView):
#     serializer_class = BanerMiddleSerializers
#     queryset = BanerMiddle.objects.all()


#     @baner_middle_get_object_from_cache(cache_key_func=baner_middle_get_cache_key)
#     def retrieve(self, request, *args, **kwargs):
#         cached_instance = kwargs.get('baner_middle_cached_instance')
#         if cached_instance is not None:
#             return Response(cached_instance, status=status.HTTP_200_OK)
#         else:
#             instance = get_object_or_404(BanerMiddle, pk=self.kwargs.get('pk'))
#             serializer = self.get_serializer(instance)
#             cache_key = baner_middle_get_cache_key(self, request, *args, **kwargs)
#             cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
#             return Response(serializer.data, status=status.HTTP_200_OK)




# class BanerMiddleUpdateApiView(generics.UpdateAPIView):
#     queryset = BanerMiddle.objects.all()
#     serializer_class = BanerMiddleSerializers

   
        
    
# class BanerMiddleDeleteApiView(generics.DestroyAPIView):
#     queryset = BanerMiddle.objects.all()
#     serializer_class = BanerMiddleSerializers

# #==  Baner Book ===============================================================================================================================================



# class BanerBookCreateApiView(generics.CreateAPIView):
#     # queryset = BanerBook.objects.all()
#     serializer_class = BanerBookSerializers

#     def perform_create(self, serializer):
#         baner_instance = serializer.save()
#         # Сохраняем идентификатор объекта в кеше
#         cache_key = 'baner_book_ids'
#         cached_ids = cache.get(cache_key, [])
#         cached_ids.append(baner_instance.pk)
#         cache.set(cache_key, cached_ids,timeout=CACHE_TIME)
#         print(f"Добавлен обьект в кеш: ",cached_ids )


# @method_decorator(baner_book_update_cache_on_expiry('baner_book_ids'), name='dispatch')
# class BanerBookListApiView(generics.ListAPIView):
#     # queryset = BanerBook.objects.all()
#     serializer_class = BanerBookSerializers

#     def get_queryset(self):
#         cache_key = 'baner_book_ids'
#         cached_ids = cache.get(cache_key, [])
#         print(cached_ids)
#         return BanerBook.objects.filter(pk__in=cached_ids)

# class BanerBookDetailApiView(generics.RetrieveAPIView):
#     queryset = BanerBook.objects.all()
#     serializer_class = BanerBookSerializers

#     @baner_book_get_object_from_cache(cache_key_func=baner_book_get_cache_key)
#     def retrieve(self, request, *args, **kwargs):
#         cached_instance = kwargs.get('baner_book_cached_instance')
#         if cached_instance is not None:
#             return Response(cached_instance, status=status.HTTP_200_OK)
#         else:
#             instance = get_object_or_404(BanerBook, pk=self.kwargs.get('pk'))
#             serializer = self.get_serializer(instance)
#             cache_key = baner_book_get_cache_key(self, request, *args, **kwargs)
#             cache.set(cache_key, serializer.data, timeout=CACHE_TIME)
#             return Response(serializer.data, status=status.HTTP_200_OK)




# class BanerBookUpdateApiView(generics.UpdateAPIView):
#     queryset = BanerBook.objects.all()
#     serializer_class = BanerBookSerializers

   


# class BanerBookDeleteApiView(generics.DestroyAPIView):
#     queryset = BanerBook.objects.all()
#     serializer_class = BanerBookSerializers

#     @baner_book_get_object_from_cache(cache_key_func=baner_book_get_cache_key)
#     def delete(self, request, *args, **kwargs):
#         cached_instance = kwargs.get('baner_book_cached_instance')
#         instance = self.get_object() if cached_instance is None else cached_instance

#         # Удаляем объект из базы данных
#         instance.delete()

#         # Удаляем объект из кеша
#         cache_key = baner_book_get_cache_key(self, request, *args, **kwargs)
#         cache.delete(cache_key)

#         # Возвращаем успешный ответ
#         return Response({"delete":"удалено!"},status=status.HTTP_204_NO_CONTENT)


