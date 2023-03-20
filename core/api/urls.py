from django.urls import path, include, re_path
from rest_framework import routers

from core.api.views import *

router = routers.SimpleRouter()

router.register('system_quide_api_urls', SystemQuideViewSet, basename='system_quide_api_urls')
router.register('faculty_api_urls', FacultyViewSet, basename='faculty_api_urls')
router.register('department_api_urls', DepartmentQuideViewSet, basename='department_api_urls')
router.register('groups_api_urls', StudentGroupQuideViewSet, basename='groups_api_urls')
router.register('students_api_urls', StudentViewSet, basename='students_api_urls')
router.register('teacher_api_urls', TeacherViewSet, basename='teacher_api_urls')

app_name = 'core_api_urls'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),

    path('students_csv_import/', StudentsCsvImport.as_view(), name='students_csv_import_url')
]

urlpatterns += router.urls