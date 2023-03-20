from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, SerializerMethodField, CurrentUserDefault, CharField
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.educational_materials.models import Discipline, DisciplineAccess, Topic, TopicVideo, TopicMaterial, \
    TopicAccess, Question, Answer
from core.api.serializers import StudentGroupQuideSerializer, DepartmentQuideSerializer
from core.models import MainUser, Teacher, StudentGroupQuide


class DisciplineTopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        exclude = ['description', ]

class MainDisciplineAccessSerialser(ModelSerializer):

    class Meta:
        model = DisciplineAccess
        exclude = ['parent_id', ]

    def __init__(self, *args, **kwargs, ):
        super(MainDisciplineAccessSerialser, self).__init__(*args, **kwargs)
        groups = DisciplineAccess.objects.filter(parent_id_id=self.context.get('discipline_id'))
        self.fields['group_id'].queryset = StudentGroupQuide.objects.all().exclude(name__in=list(groups))

class DisciplineAccessSerialser(MainDisciplineAccessSerialser):
    group_id = StudentGroupQuideSerializer()


class DisciplineSerializer(ModelSerializer):
    discipline_access_parent_id = DisciplineAccessSerialser(read_only=True, many=True)
    department_id = DepartmentQuideSerializer(read_only=True)
    topic_discipline_id = DisciplineTopicSerializer(read_only=True, many=True)

    class Meta:
        model = Discipline
        fields = ['pk', 'department_id', 'creation_date', 'title', 'description', 'program', 'status',
                  'get_quiz_questions', 'get_themes', 'discipline_access_parent_id', 'topic_discipline_id', ]

class TopicDisciplineSerializer(ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['pk', 'department_id', 'title', 'status', ]

class TopicVideoSerializer(ModelSerializer):
    class Meta:
        model = TopicVideo
        fields = '__all__'
        read_only_fields = ['topic_id']

class TopicMaterialSerializer(ModelSerializer):
    class Meta:
        model = TopicMaterial
        fields = '__all__'
        read_only_fields = ['topic_id']

class TopicAccessSerializer(ModelSerializer):
    class Meta:
        model = TopicAccess
        exclude = ['parent_id', ]

    def __init__(self, *args, **kwargs, ):
        super(TopicAccessSerializer, self).__init__(*args, **kwargs)
        if self.context.get('topic_id') is not None:
            discipline = Topic.objects.get(pk=self.context.get('topic_id'))
            aviable_groups = DisciplineAccess.objects.filter(parent_id=discipline.discipline_id)
            disabled_groups = TopicAccess.objects.filter(parent_id=discipline)
            self.fields['group_id'].queryset = StudentGroupQuide.objects.all().filter(name__in=list(aviable_groups)) \
                .exclude(name__in=list(disabled_groups))

class GroupseTopicAccessSerializer(TopicAccessSerializer):
    group_id = StudentGroupQuideSerializer(read_only=True,)

class TopicSerializer(ModelSerializer):
    discipline_id = TopicDisciplineSerializer(read_only=True,)
    topic_video_topic_id = TopicVideoSerializer(read_only=True, many=True)
    topic_material_topic_id = TopicMaterialSerializer(read_only=True, many=True)
    topic_access_parent_id = GroupseTopicAccessSerializer(read_only=True, many=True)

    class Meta:
        model = Topic
        fields = ['discipline_id', 'get_quiz_questions', 'pk', 'creation_date', 'title', 'description', 'status',
                  'topic_video_topic_id', 'topic_material_topic_id', 'topic_access_parent_id',]

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['topic_access', ]
class QuestionSerializer(ModelSerializer):
    answer_question_id = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['topic_access', 'answer_question_id']

class QuestionCopySerializer(Serializer):
    topic_to = ChoiceField([])

    def __init__(self, *args, **kwargs,):
        super(QuestionCopySerializer, self).__init__(*args, **kwargs)
        department = Teacher.objects.get(pk=self.context.get("request").user.pk).deaprtment_id
        self.fields['topic_to'].choices = list(Topic.objects.filter(discipline_id__department_id=department))

class QuestionAnswerSerializer(ModelSerializer):
    #answer_question_id = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'variants_type']
class AnswerEditSerializer(ModelSerializer):
    question_id = QuestionAnswerSerializer(read_only=True, )

    class Meta:
        model = Answer
        fields = ['pk', 'question_id', 'ansr_text', 'answer_right',]


class AnswerSequenceEditSerializer(AnswerEditSerializer):

    class Meta(AnswerEditSerializer.Meta):
        fields = ['pk', 'question_id', 'ansr_text', 'first_columnn', ]

    def validate(self, data,):
        if self.instance:
            if self.instance.question_id.answer_question_id.count() < data['first_columnn']:
                raise ValidationError('Invalid position for answer')

        return data

class AnswerSecondColumnComplianceSerializer(AnswerSequenceEditSerializer):

    class Meta(AnswerSequenceEditSerializer.Meta):
        fields = ['pk', 'question_id', 'ansr_text', 'second_column', ]

    def validate(self, data,):
        if self.instance:
            if self.instance.question_id.answer_question_id.count() < data['second_column']:
                raise ValidationError('Invalid position for answer')

        return data

class AnswerComplianceSerializer(Serializer):
    question = CharField(label='Question', required=True)
    answer = CharField(label='Answer', required=True)