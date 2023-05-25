from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from core.models import *

class SystemQuideSerializer(ModelSerializer):

    class Meta:
        model = SystemQuide
        fields = '__all__'

class FacultyQuideSerializer(ModelSerializer):

    class Meta:
        model = FacultyQuide
        fields = ['name', 'url',]
        extra_kwargs = {
            'url': {'view_name': 'core_urls:faculty_api_urls-detail', 'lookup_field': 'pk'},
        }

class DepartmentQuideSerializer(ModelSerializer):
    faculty_name = serializers.ReadOnlyField(source='faculty_id.name')

    class Meta:
        model = DepartmentQuide
        fields = ['faculty_id', 'faculty_name', 'name', 'url']
        extra_kwargs = {
            'url': {'view_name': 'core_urls:department_api_urls-detail', 'lookup_field': 'pk'},
        }

class StudentGroupQuideSerializer(ModelSerializer):
    faculty_name = serializers.ReadOnlyField(source='faculty_id.name')

    class Meta:
        model = StudentGroupQuide
        fields = DepartmentQuideSerializer.Meta.fields
        extra_kwargs = {
            'url': {'view_name': 'core_urls:groups_api_urls-detail', 'lookup_field': 'pk'},
        }

user_fields = ['pk', 'first_name', 'last_name', 'patronymic', 'email', 'username', 'url', ]

class StudentSerializer(ModelSerializer):
    active_group = serializers.ReadOnlyField(source='active_group_id.name')

    class Meta:
        model = Student
        fields = user_fields + ['active_group', 'all_group_id', 'grade_book_number', ]
        extra_kwargs = {
            'url': {'view_name': 'core_urls:students_api_urls-detail', 'lookup_field': 'pk'},
        }


class TeacherSerializer(ModelSerializer):
    deaprtment = serializers.ReadOnlyField(source='deaprtment_id.name')

    class Meta:
        model = Teacher
        fields = user_fields + ['deaprtment', 'all_department_id', ]
        extra_kwargs = {
            'url': {'view_name': 'core_urls:teacher_api_urls-detail', 'lookup_field': 'pk'},
        }

class MyUserSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = MainUser
        fields = '__all__'

class StudentsCsvImportSerializer(Serializer):
    file = serializers.FileField()
