"""kahluaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/users/', include('dj_rest_auth.urls')),
    path('api/users/', include('allauth.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/application/', include('application.urls')),
    path('api/kahlua_admin/', include('kahlua_admin.urls')),
]

# API 문서에 작성될 소개 내용
schema_view = get_schema_view(
    openapi.Info(
        title='KAHLUABAND OPEN API',
        default_version='v1',
        description='''
            안녕하세요. KAHLUABAND OPEN API 문서 페이지입니다.
        ''',
        terms_of_service='',
        contact=openapi.Contact(name='KAHLUA_BAND', email='hcbkahlua@gmail.com'),
        license=openapi.License(name='KAHLUA_BAND')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
)

urlpatterns += [
    path('swagger<str:format>', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]