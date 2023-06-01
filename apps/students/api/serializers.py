from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.educational_materials.models import Discipline, DisciplineAccess, TopicAccess, Topic, TopicVideo, \
    TopicMaterial
from core.models import Student


class StudentRegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = Student
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'last_login', 'date_joined',
                   'all_group_id', ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(StudentRegisterSerializer, self).create(validated_data)

class DisciplinesListSerializer(ModelSerializer):

    class Meta:
        model = Discipline
        fields = ['pk', 'title', 'get_themes', ]

class DisciplinesSerializer(ModelSerializer):
    parent_id = DisciplinesListSerializer()

    class Meta:
        model = DisciplineAccess
        fields = ['parent_id', 'pk', 'discipline_access_start', 'discipline_access_end', 'test_quize_start', 'test_quize_end',
                  'final_quize_start', 'final_quize_end', 'get_quize_access', 'url']
        extra_kwargs = {
            'url': {'view_name': 'students_urls:discipline_detail', 'lookup_field': 'pk'},
        }

class ToppicListSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = ['pk', 'title', ]

class TopicAccessListSerializer(ModelSerializer):
    parent_id = ToppicListSerializer()

    class Meta:
        model = TopicAccess
        fields = DisciplinesSerializer.Meta.fields
        extra_kwargs = {
            'url': {'view_name': 'students_urls:topic_detail', 'lookup_field': 'pk'},
        }


class DisciplinesFullSerializer(ModelSerializer):
    get_themes_access = TopicAccessListSerializer(many=True)

    class Meta:
        model = Discipline
        fields = ['pk', 'title', 'description', 'program', 'get_themes', 'get_themes_access', ]

class DisciplineSerializer(ModelSerializer):
    parent_id = DisciplinesFullSerializer()

    class Meta:
        model = DisciplineAccess
        fields = ['parent_id', 'pk', 'discipline_access_start', 'discipline_access_end', 'test_quize_start',
                  'test_quize_end',
                  'final_quize_start', 'final_quize_end', 'get_quize_access', ]


class StudentTopicVideoSerializer(ModelSerializer):

    class Meta:
        model = TopicVideo
        exclude = ['topic_id']

class StudentTopicMaterialSerializer(ModelSerializer):

    class Meta:
        model = TopicMaterial
        exclude = ['topic_id']

class TopicDetailSerializer(ModelSerializer):
    discipline_id = DisciplinesListSerializer()
    topic_video_topic_id = StudentTopicVideoSerializer(many=True)
    topic_material_topic_id = StudentTopicMaterialSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['pk', 'creation_date', 'title', 'description', 'discipline_id', 'topic_video_topic_id',
                  'topic_material_topic_id',]

class TopicAccessDetailSerializer(ModelSerializer):
    parent_id = TopicDetailSerializer()

    class Meta:
        model = TopicAccess
        fields = ['pk',  'discipline_access_start', 'discipline_access_end', 'test_quize_start', 'test_quize_end',
                  'final_quize_start', 'final_quize_end', 'parent_id',]
