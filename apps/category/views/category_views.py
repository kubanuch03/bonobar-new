from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from django.db.utils import DatabaseError
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from ..models import Category
from ..serializers import CategorySerializer
from mixins.mixins import RequiredParamsMixin
from apps.category.cache.cache_category import get_object_from_cache, get_cache_key, delete_object_from_cache, cache_get_response

logger = logging.getLogger(__name__)

CACHE_TIME = settings.CACHE_TIME


class CategoryListCreateAPIView(RequiredParamsMixin, APIView):
    required_params = ['name',]

    @swagger_auto_schema(
        operation_description="Retrieve a list of categories",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    @swagger_auto_schema(
        operation_description="Post category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Category image')
            },
            required=['name']
        ),
        responses={201: openapi.Response('Created category', CategorySerializer)}
    )
    def post(self, request):
        missing_params_response = self.check_required_params(request.data)
        if missing_params_response:
            return missing_params_response

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_instance = serializer.save()

            cache_key = 'category_ids'
            cached_ids = cache.get(cache_key, [])
            cached_ids.append(category_instance.pk)
            cache.set(cache_key, cached_ids, timeout=CACHE_TIME)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):

    @get_object_from_cache(get_cache_key)
    @swagger_auto_schema(
        operation_description="Get category by pk. Pk has to be category_id.",
        responses={200: openapi.Response("Category detail parameters.", CategorySerializer(many=True))}
    )
    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Category image')
            },
        ),
        responses={200: CategorySerializer(), 400: "Bad request"}
    )
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a category",
        responses={204: "Category deleted successfully.", 404: "Not found."}
    )
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@swagger_auto_schema(
    operation_description="List categories with their subcategories",
    responses={200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'subcategories': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    ))}
)
def category_subcategory_list(request):
    cache_key = 'category_subcategory_list'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    try:
        categories = Category.objects.all().prefetch_related('subcategories')
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return JsonResponse({'error': 'Database error'}, status=500)

    data = []
    try:
        for category in categories:
            subcategories = category.subcategories.all()
            subcategory_list = [{'id': subcat.id, 'name': subcat.name} for subcat in subcategories]

            data.append({
                'id': category.id,
                'name': category.name,
                'subcategories': subcategory_list
            })
    except Exception as e:
        logger.error(f"Error processing categories: {e}")
        return JsonResponse({'error': 'Error processing categories'}, status=500)

    try:
        cache.set(cache_key, data, timeout=CACHE_TIME)
    except Exception as e:
        logger.error(f"Error setting cache: {e}")
        return JsonResponse({'error': 'Error setting cache'}, status=500)

    return JsonResponse(data, safe=False)


@swagger_auto_schema(
    method='get',
    operation_description="List subcategories for a given category",
    manual_parameters=[
        openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                          required=True, description='ID of the category to list subcategories for')
    ],
    responses={
        200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )),
        400: "Bad request",
        404: "Category not found",
        500: "Internal server error"
    }
)
@api_view(['GET'])
def subcategory_list(request):
    category_id = request.GET.get('category_id', None)
    if not category_id:
        return JsonResponse({'error': 'Category parameter is required'}, status=400)

    cache_key = f'subcategory_list_{category_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    try:
        category = Category.objects.prefetch_related('subcategories').get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return JsonResponse({'error': 'Database error'}, status=500)

    subcategories = category.subcategories.all().values('id', 'name')
    subcategory_list = list(subcategories)

    try:
        cache.set(cache_key, subcategory_list, timeout=CACHE_TIME)
    except Exception as e:
        logger.error(f"Error setting cache: {e}")
        return JsonResponse({'error': 'Error setting cache'}, status=500)

    return JsonResponse(subcategory_list, safe=False)
