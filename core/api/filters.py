import django_filters
from django_filters import ModelChoiceFilter

from core.models import *


class FacultyFilter(django_filters.FilterSet):

    class Meta:
        model = FacultyQuide
        fields = {
            'name': ['startswith', ],
        }

class DepartmentQuideFilter(django_filters.FilterSet):
    faculty_id = ModelChoiceFilter(queryset=FacultyQuide.objects.all(), label=('Kафедрa'),)

    class Meta:
        model = DepartmentQuide
        fields = {
            'name': ['startswith', ],
        }

class StudentGroupQuideFilter(DepartmentQuideFilter):

    class Meta(DepartmentQuideFilter.Meta):
        model = StudentGroupQuide

class StudentFilter(django_filters.FilterSet):
    all_group_id = ModelChoiceFilter(queryset=StudentGroupQuide.objects.all(), label=('Группа'),)

    class Meta:
        model = Student
        fields = {
            'username': ['startswith', ],
            'first_name': ['startswith', ],
            'email': ['startswith', ],
        }

class TeasherFilter(django_filters.FilterSet):
    all_department_id = ModelChoiceFilter(queryset=DepartmentQuide.objects.all(), label=('Кафедра'),)

    class Meta(StudentFilter.Meta):
        model = Teacher
