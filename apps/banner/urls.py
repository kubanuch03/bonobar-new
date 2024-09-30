from django.urls import path
from .views import *


urlpatterns = [

    #BanerMain
    path("list/banner/", BanerMainListApiView.as_view(),name='list_banner'),
    path("create/banner/", BanerMainCreateApiView.as_view(),name='create_banner'),
    path("detail/banner/<int:pk>/", BanerMainDetailApiView.as_view(),name='detail_banner'),
    path("delete/banner/<int:pk>/", BanerMainDeleteApiView.as_view(),name='delete_banner'),
    path("update/banner/<int:pk>/", BanerMainUpdateApiView.as_view(),name='update_banner'),

    #BanerMainTopik
    path("list/banner/topik/", BanerMainTopikListApiView.as_view(),name='list_banner_topk'),
    path("create/banner/topik/", BanerMainTopikCreateApiView.as_view(),name='create_banner_topk'),
    path("detail/banner/topik/<int:pk>/", BanerMainTopikDetailApiView.as_view(),name='detail_banner_topk'),
    path("delete/banner/topik/<int:pk>/", BanerMainTopikDeleteApiView.as_view(),name='delete_banner_topk'),
    path("update/banner/topik/<int:pk>/", BanerMainTopikUpdateApiView.as_view(),name='update_banner_topk'),

    # #BanerMiddle
    # path('list/baner/middle/', BanerMiddleListApiView.as_view(),name='list_baner_middle'),
    # path('create/baner/middle/', BanerMiddleCreateApiView.as_view(),name='create_baner_middle'),
    # path("detail/banner/middle/<int:pk>/", BanerMiddleDetailApiView.as_view(),name='detail_banner_middle'),
    # path("delete/banner/middle/<int:pk>/", BanerMiddleDeleteApiView.as_view(),name='delete_banner_middle'),
    # path("update/banner/middle/<int:pk>/", BanerMiddleUpdateApiView.as_view(),name='update_banner_middle'),

    # #BanerBook
    # path('list/baner/book/', BanerBookListApiView.as_view(),name='list_baner_book'),
    # path('create/baner/book/', BanerBookCreateApiView.as_view(),name='create_baner_book'),
    # path("detail/banner/book/<int:pk>/", BanerBookDetailApiView.as_view(),name='detail_banner_book'),
    # path("delete/banner/book/<int:pk>/", BanerBookDeleteApiView.as_view(),name='delete_banner_book'),
    # path("update/banner/book/<int:pk>/", BanerBookUpdateApiView.as_view(),name='update_banner_book'),
]
