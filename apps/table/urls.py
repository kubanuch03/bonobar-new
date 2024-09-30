from django.urls import path
from .views import *

urlpatterns = [
    path('list/table/',TableListApiView.as_view(),name='list/table'),
    path('create/table/',TableCreateApiView.as_view(),name='create/table'),
    path('detail/table/<int:pk>/',TableDetailApiView.as_view(),name='detail/table'),
    path('update/table/<int:pk>/',TableUpdateApiView.as_view(),name='update/table'),
    path('delete/table/<int:pk>/',TableDeleteApiView.as_view(),name='delete/table'),
]
