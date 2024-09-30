from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import Http404
from django.core.cache import cache
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from ..serializers.subcategory_serializer import SubCategorySerializer, SubCategoryOrderSerializer
from ..cache.cache_subcategory import cache_get_response, get_object_from_cache, get_cache_key, delete_object_from_cache
from ..models import SubCategory

CACHE_TIME = settings.CACHE_TIME


class SubCategoryListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a list of subcategories.",
        responses={200: SubCategorySerializer(many=True)},
    )
    def get(self, request):
        subcategories = SubCategory.objects.all().order_by('order')
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a subcategory",
        request_body=SubCategorySerializer,
        responses={201: SubCategorySerializer(), 400: "Bad request"}
    )
    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            subcategory_instance = serializer.save()

            cache_key = 'subcategory_ids'
            cached_ids = cache.get(cache_key, [])
            cached_ids.append(subcategory_instance.pk)
            cache.set(cache_key, cached_ids, timeout=CACHE_TIME)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            raise Http404

    @get_object_from_cache(get_cache_key)
    @swagger_auto_schema(
        operation_description="Get subcategory by pk. Pk has to be category_id.",
        responses={200: openapi.Response("Subcategory detail parameters.", SubCategorySerializer(many=True))}
    )
    def get(self, request, pk):
        subcategory = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update subcategory",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Subcategory name'),
                'parent': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID')
            },
        ),
        responses={200: SubCategorySerializer(), 400: "Bad request"}
    )
    def put(self, request, pk):
        subcategory = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a subcategory",
        responses={204: "Subcategory deleted successfully.", 404: "Not found."}
    )
    def delete(self, request, pk):
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response({"detail": "Subcategory deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class SubCategoryOrderUpdateAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Изменение порядка подкатегорий",
        request_body=SubCategoryOrderSerializer(many=True),
        responses={200: "Порядок подкатегорий обновлен.", 400: "Неверный запрос"}
    )
    def post(self, request):
        serializer = SubCategoryOrderSerializer(data=request.data, many=True)
        if serializer.is_valid():
            for item in serializer.validated_data:
                subcategory = SubCategory.objects.get(pk=item['id'])
                subcategory.order = item['order']
                subcategory.save()
            return Response({"detail": "Порядок подкатегорий обновлен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    