from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from core.api.filters import *
from core.api.serializers import *
from core.core import students_import_from_csv
from core.models import *

class SystemQuideViewSet(ModelViewSet):
    """
        отображает и редактирует системный справочник настроек.
        permission_classes = (IsAdminUser,)
    """
    queryset = SystemQuide.objects.all().order_by('id')
    serializer_class = SystemQuideSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace']

class CorePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class FacultyViewSet(ModelViewSet):
    """
        Перечисляет и редактирует факультеты.
        permission_classes = (IsAdminUser,)
    """
    queryset = FacultyQuide.objects.all().order_by('id')
    serializer_class = FacultyQuideSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CorePagination
    filterset_class = FacultyFilter

class DepartmentQuideViewSet(FacultyViewSet):
    """
        Перечисляет и редактирует кафедры.
        permission_classes = (IsAdminUser,)

    """
    queryset = DepartmentQuide.objects.all().order_by('id')
    serializer_class = DepartmentQuideSerializer
    filterset_class = DepartmentQuideFilter

class StudentGroupQuideViewSet(DepartmentQuideViewSet):
    """
        Перечисляет и редактирует Группы студентов.
        permission_classes = (IsAdminUser,)

    """
    queryset = StudentGroupQuide.objects.all().order_by('id')
    serializer_class = StudentGroupQuideSerializer
    filterset_class = StudentGroupQuideFilter

class StudentViewSet(DepartmentQuideViewSet):
    """
        Перечисляет и редактирует студентов.
        permission_classes = (IsAdminUser,)

    """
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    filterset_class = StudentFilter

class TeacherViewSet(DepartmentQuideViewSet):
    """
        Перечисляет и редактирует студентов.
        permission_classes = (IsAdminUser,)

    """
    queryset = Teacher.objects.all().order_by('id')
    serializer_class = TeacherSerializer
    filterset_class = TeasherFilter

class StudentsCsvImport(APIView):
    """
        импотриует студентов из файла csv.
        permission_classes = (IsAdminUser,)

    """
    serializer_class = StudentsCsvImportSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = StudentsCsvImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result_string = students_import_from_csv(serializer.validated_data['file'])

        return Response({"status": result_string},
                        status.HTTP_201_CREATED)