

from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Bono Bar",
      default_version='v1',
      description="API description",
    #   terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="admin"),
      license=openapi.License(name="Digital Forge Tech License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   # url='http://3.123.17.71/',
)

urlpatterns = [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]