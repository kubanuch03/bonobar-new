from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GalleryListCreate, GalleryDetailAPIView

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path('galleries/', GalleryListCreate.as_view(), name='galleries'),
    path('gallery_detail/<int:pk>/', GalleryDetailAPIView.as_view(), name='gallery_detail'),
]

app_name = 'gallery'
