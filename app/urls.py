"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.flatpages import views
from app import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="My educational Portal API",
      default_version='v1',
      description="My educational Portal API",
      terms_of_service="No terms",
      contact=openapi.Contact(email="hamster197@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

handler403 = 'app.views.v404_view'
handler404 = 'app.views.v404_view'
handler500 = 'app.views.v404_view'


urlpatterns = [
    re_path('swagger(\.json|\.yaml)/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0, ), name='schema-swagger-ui',),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('select2/', include("django_select2.urls")),
    path('', views.flatpage,  {'url': '/main/'}, name='main'),

    path('portal/', include('apps.portal.urls')),
    path('core/', include('core.urls')),
    path('teacher/', include('apps.teachers.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
