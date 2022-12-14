"""zzikmuk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from . import settings
# from .. import static

schema_view = get_schema_view(
    openapi.Info(
        title="ZZIKMUK(찍먹)",
        default_version="v1",
        description="찍먹 서비스의 API 문서입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public = True,
    permission_classes = (AllowAny,),
)

urlpatterns = [
    # Swagger API 설정 url
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    # 여기서부터 사용하는 주소
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('receipts/', include('receipts.urls')),
    path('languages/', include('languages.urls')),
 ] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)