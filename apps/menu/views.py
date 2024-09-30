from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from .models import Menu
from .serializers import MenuSerializer
from mixins.mixins import RequiredParamsMixin
from .cache_menu import (
    cache_get_response, get_object_from_cache, get_cache_key,
    delete_object_from_cache
)

CACHE_TIME = settings.CACHE_TIME


class MenuListCreateAPIView(RequiredParamsMixin, APIView):
    required_params = ['title', 'price', 'image', 'category', 'subcategory']

    @swagger_auto_schema(
        operation_description="Get a list of menus",
        responses={200: MenuSerializer(many=True)}
    )
    # @cache_get_response(cache_key_func=lambda self, request: 'menu_list', timeout=CACHE_TIME)
    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new menu",
        request_body=MenuSerializer,
        responses={201: MenuSerializer(), 400: "Bad request"}
    )
    def post(self, request):
        missing_params_response = self.check_required_params(request.data)
        if missing_params_response:
            return missing_params_response

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():
            menu_instance = serializer.save()

            cache_key = 'menu_ids'
            cached_ids = cache.get(cache_key, [])
            cached_ids.append(menu_instance.pk)
            cache.set(cache_key, cached_ids, timeout=CACHE_TIME)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Get a menu detail",
        responses={200: MenuSerializer()}
    )
    @get_object_from_cache(get_cache_key)
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a menu",
        request_body=MenuSerializer,
        responses={200: MenuSerializer(), 400: "Bad request"}
    )
    def put(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a menu",
        responses={204: "Menu deleted successfully."}
    )
    def delete(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        menu.delete()
        return Response({"detail": "Menu deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class MenuListByCategory(APIView):

    @staticmethod
    def get_cache_key(request, category_id, parent_id=None, subcategory_id=None):
        return f"menus_by_category_{category_id}_parent_{parent_id}_subcategory_{subcategory_id}"

    @staticmethod
    def handle_no_menu_items():
        return Response({
            "detail": "No menu items found for the given category."
        }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Get menus by category. Example query: ?category={value}&subcategory={value}",
        responses={200: MenuSerializer(many=True), 404: "No menu items found for the given category."}
    )
    def get(self, request):
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')

        cache_key = self.get_cache_key(request, category_id, subcategory_id)
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        menus = Menu.objects.filter(category_id=category_id, subcategory_id=subcategory_id)
        if not menus.exists():
            return self.handle_no_menu_items()

        serializer = MenuSerializer(menus, many=True).data
        cache.set(cache_key, serializer, timeout=CACHE_TIME)
        return Response(serializer)
