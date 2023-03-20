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
        fields = '__all__'

class DepartmentQuideSerializer(ModelSerializer):
    faculty_name = serializers.ReadOnlyField(source='faculty_id.name')

    class Meta:
        model = DepartmentQuide
        fields = '__all__'

class StudentGroupQuideSerializer(ModelSerializer):
    faculty_name = serializers.ReadOnlyField(source='faculty_id.name')

    class Meta:
        model = StudentGroupQuide
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    active_group = serializers.ReadOnlyField(source='active_group_id.name')

    class Meta:
        model = Student
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'password',]

class TeacherSerializer(ModelSerializer):
    deaprtment = serializers.ReadOnlyField(source='deaprtment_id.name')

    class Meta(StudentSerializer.Meta):
        model = Teacher

class MyUserSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'

class StudentsCsvImportSerializer(Serializer):
    file = serializers.FileField()
