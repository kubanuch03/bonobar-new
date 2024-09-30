from django.urls import path
from .views import *

urlpatterns = [
    path('list/book/',BookListApiView.as_view(),name='list/book'),
    path('create/book/',BookCreateApiView.as_view(),name='create/book'),
    path('detail/book/<int:pk>/',BookDetailApiView.as_view(),name='detail/book/id/'),
    path('update/book/<int:pk>/',BookUpdateApiView.as_view(),name='update/book/id/'),
    path('delete/book/<int:pk>/',BookDeleteApiView.as_view(),name='delete/book/id/'),
    path('available-times/', AvailableTimesApiView.as_view(), name='available-times/'),
    path('download-booking/', DownloadBookingFileView.as_view(), name='download-booking'),
     
]