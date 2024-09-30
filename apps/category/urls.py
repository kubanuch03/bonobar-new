from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.category_views import (
    CategoryDetailAPIView, CategoryListCreateAPIView, category_subcategory_list,
    subcategory_list)

from .views.subcategory_views import SubCategoryListCreateAPIView, SubCategoryDetailAPIView, SubCategoryOrderUpdateAPIView

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path('list_or_create/', CategoryListCreateAPIView.as_view(), name='category_list_or_create'),
    path('<int:pk>/', CategoryDetailAPIView.as_view(), name='category-get--update-delete'),
    path('subcategories/', SubCategoryListCreateAPIView.as_view(), name='subcategory_list_create'),
    path('subcategories/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('category_subcategory_list/', category_subcategory_list, name='category_subcategory_list'),
    path('subcategory_list/', subcategory_list, name='subcategory_list'),
    path('subcategories/order/', SubCategoryOrderUpdateAPIView.as_view(), name='subcategory-order-update'),
]

app_name = 'category'
