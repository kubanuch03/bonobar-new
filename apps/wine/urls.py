from django.urls import path
from .views import WineListCreateAPIView, WineDetailAPIView

urlpatterns = [
    path('wines/', WineListCreateAPIView.as_view(), name='wine_list_create'),
    path('wines/<int:pk>/', WineDetailAPIView.as_view(), name='wine_detail_get_delete'),
]
