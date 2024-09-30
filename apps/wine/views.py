from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from .models import Wine
from .serializers import WineSerializer
from .wine_cache import cache_response


class WineListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of wines",
        responses={200: WineSerializer(many=True)}
    )
    @cache_response('wine_list')
    def get(self, request):
        wines = Wine.objects.all()
        serializer = WineSerializer(wines, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new wine",
        request_body=WineSerializer,
        responses={201: WineSerializer(), 400: "Bad request"}
    )
    def post(self, request):
        serializer = WineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('wine_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WineDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get wine detail",
        responses={200: WineSerializer()}
    )
    @cache_response('wine_detail_{pk}')
    def get(self, request, pk):
        wine = get_object_or_404(Wine, pk=pk)
        serializer = WineSerializer(wine)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update wine detail",
        request_body=WineSerializer,
        responses={200: WineSerializer(), 400: "Bad request"}
    )
    def put(self, request, pk):
        wine = get_object_or_404(Wine, pk=pk)
        serializer = WineSerializer(wine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete('wine_list')
            cache.delete(f'wine_detail_{pk}')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a wine",
        responses={204: "Wine deleted successfully."}
    )
    def delete(self, request, pk):
        wine = get_object_or_404(Wine, pk=pk)
        wine.delete()
        cache.delete('wine_list')
        cache.delete(f'wine_detail_{pk}')
        return Response({"detail": "Wine deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
