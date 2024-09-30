from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import Gallery
from .serializers import GallerySerializer


class GalleryListCreate(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Retrieve a list of galleries",
        responses={200: GallerySerializer(many=True)},
    )
    def get(self, request):
        galleries = Gallery.objects.all()
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new gallery",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, description='Gallery title', type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_FORM, description='Gallery description. Not required.', type=openapi.TYPE_STRING),
            openapi.Parameter('image', openapi.IN_FORM, description='Gallery image', type=openapi.TYPE_FILE)
        ],
        responses={201: GallerySerializer(many=True), 400: "Bad request"},
    )
    def post(self, request, *args, **kwargs):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('galleries')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a gallery detail",
        responses={200: GallerySerializer()},
    )
    def get(self, request, pk):
        cache_key = f'gallery_{pk}'
        gallery_data = cache.get(cache_key)

        if not gallery_data:
            gallery = get_object_or_404(Gallery, pk=pk)
            serializer = GallerySerializer(gallery)
            gallery_data = serializer.data
            cache.set(cache_key, gallery_data, timeout=20)
        return Response(gallery_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a gallery detail",
        request_body=GallerySerializer,
        responses={200: GallerySerializer(), 400: "Bad request"},
    )
    def put(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        serializer = GallerySerializer(gallery, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            gallery_data = serializer.data
            return Response(gallery_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a gallery",
        responses={204: "Gallery deleted."},
    )
    def delete(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        gallery.delete()
        cache_key = f'gallery_{pk}'
        cache.delete(cache_key)
        return Response({
            "message": "Gallery deleted.",
        }, status=status.HTTP_204_NO_CONTENT)
