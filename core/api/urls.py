from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.api.views import *

router = routers.SimpleRouter()

router.register('system_quide_api_urls', SystemQuideViewSet, basename='system_quide_api_urls')
router.register('faculty_api_urls', FacultyViewSet, basename='faculty_api_urls')
router.register('department_api_urls', DepartmentQuideViewSet, basename='department_api_urls')
router.register('groups_api_urls', StudentGroupQuideViewSet, basename='groups_api_urls')
router.register('students_api_urls', StudentViewSet, basename='students_api_urls')
router.register('teacher_api_urls', TeacherViewSet, basename='teacher_api_urls')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('students_csv_import/', StudentsCsvImport.as_view(), )
]

urlpatterns += router.urls