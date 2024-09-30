from django.urls import path
from .views import *


urlpatterns = [
    path('list/floor/',FloorListApiView.as_view(),name='list_floor'),
    path('create/floor/',FloorCreateApiView.as_view(),name='create_floor'),
    path('detail/floor/<int:pk>/',FloorDetailApiView.as_view(),name='detail_floor'),
    path('update/floor/<int:pk>/',FloorUpdateApiView.as_view(),name='update_floor'),
    path('delete/floor/<int:pk>/',FloorDeleteApiView.as_view(),name='delete_floor'),
]