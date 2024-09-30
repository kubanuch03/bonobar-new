from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MenuListCreateAPIView, MenuDetailAPIView, MenuListByCategory


router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path('list_or_create/', MenuListCreateAPIView.as_view(), name='menu_list_or_create'),
    path('get_update_or_delete/<int:pk>/', MenuDetailAPIView.as_view(), name='menu_get_update_or_delete'),
    path('menu_list_by_category_subcategory/', MenuListByCategory.as_view(), name='menu_list_by_category')
]

app_name = 'menu'
