from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, CharField, SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.educational_materials.models import Discipline, DisciplineAccess, Topic, TopicVideo, TopicMaterial, \
    TopicAccess, Question, Answer
from core.api.core import ParameterisedHyperlinkedIdentityField
from core.api.serializers import StudentGroupQuideSerializer, DepartmentQuideSerializer
from core.models import Teacher, StudentGroupQuide, Student


class DisciplineTopicSerializer(ModelSerializer):

    topic_url = ParameterisedHyperlinkedIdentityField(view_name='teacher_urls:topic_api_urls-detail',
                                                       lookup_fields=(('pk', 'pk'), ('discipline_id.pk', 'discipline_id')),
                                                       read_only=True)
    class Meta:
        model = Topic
        fields = ['pk', 'title', 'status', 'get_quiz_questions', 'topic_url']

class MainDisciplineAccessSerialser(ModelSerializer):

    class Meta:
        model = DisciplineAccess
        exclude = ['parent_id', ]

    def __init__(self, *args, **kwargs, ):
        super(MainDisciplineAccessSerialser, self).__init__(*args, **kwargs)
        groups = DisciplineAccess.objects.filter(parent_id_id=self.context.get('discipline_id'))\
            .values_list('group_id__name', flat=True)
        self.fields['group_id'].queryset = StudentGroupQuide.objects.all().\
            exclude(name__in=groups.exclude(group_id=self.context.get('self_group')))

class DisciplineAccessHyperLinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        if obj.group_id.pk is None:
            return None

        return self.reverse(view_name, kwargs={
            'group_id': obj.group_id.pk, 'instance_id': obj.pk,
        }, format=format, request=request)

class DisciplineAccessSerialser(ModelSerializer):
    group_id = StudentGroupQuideSerializer()
    access_url = ParameterisedHyperlinkedIdentityField(view_name='teacher_urls:discipline_access_api_urls-detail',
                                        lookup_fields=(('pk', 'pk'), ('parent_id.pk', 'discipline_id')), read_only=True)
    rezult_url = DisciplineAccessHyperLinkedIdentityField(view_name='teacher_urls:report_card_decepline')

    class Meta:
        model = DisciplineAccess
        fields = ['pk', 'group_id', 'quiestion_quantity', 'time', 'discipline_access_start', 'discipline_access_end',
                  'test_quize_start', 'test_quize_end', 'final_quize_start', 'final_quize_end', 'access_url', 'rezult_url',]


class DisciplineSerializer(ModelSerializer):
    discipline_access_parent_id = DisciplineAccessSerialser(read_only=True, many=True)
    department_id = DepartmentQuideSerializer(read_only=True)
    topic_discipline_id = DisciplineTopicSerializer(read_only=True, many=True)

    class Meta:
        model = Discipline
        fields = ['pk', 'department_id', 'creation_date', 'title', 'description', 'program', 'status',
                  'get_quiz_questions', 'get_themes', 'discipline_access_parent_id', 'topic_discipline_id', ]

class DisciplineAccessListSerialser(DisciplineAccessSerialser):

    class Meta(MainDisciplineAccessSerialser.Meta):
        fields = ['group_id', ]
        exclude = None

class TeacherDisciplinesListSerializer(ModelSerializer):
    discipline_access_parent_id = DisciplineAccessListSerialser(read_only=True, many=True)

    class Meta:
        model = Discipline
        fields = ['pk',  'creation_date', 'title', 'get_quiz_questions', 'get_themes', 'discipline_access_parent_id',
                  'url']

    def get_extra_kwargs(self):
        if 'published' in self.context:
            extra_kwargs = {
                'url': {'view_name': 'teacher_urls:discipline_published_api_urls-detail', 'lookup_field': 'pk'},
            }
        else:
            extra_kwargs = {
                'url': {'view_name': 'teacher_urls:discipline_unpublished_api_urls-detail', 'lookup_field': 'pk'},
            }
        return extra_kwargs

class TopicDisciplineSerializer(ModelSerializer):

    class Meta:
        model = Discipline
        fields = ['pk', 'department_id', 'title', 'status', 'url']
        extra_kwargs = {
            'url': {'view_name': 'teacher_urls:discipline_published_api_urls-detail', 'lookup_field': 'pk'},
        }

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

class TopicAccessHyperLinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        if obj.group_id.pk is None:
            return None

        return self.reverse(view_name, kwargs={
            'group_id': obj.group_id.pk, 'instance_id': obj.pk,
        }, format=format, request=request)

class TopicAccessSerializer(ModelSerializer):
    access_url = ParameterisedHyperlinkedIdentityField(view_name='teacher_urls:topic_access_api_urls-detail',
                                                       lookup_fields=(('pk', 'pk'), ('parent_id.pk', 'topic_id')),
                                                       read_only=True)
    rezult_url = TopicAccessHyperLinkedIdentityField(view_name='teacher_urls:report_card_topic')

    class Meta:
        model = TopicAccess
        exclude = ['parent_id', ]

    def __init__(self, *args, **kwargs,):
        super(TopicAccessSerializer, self).__init__(*args, **kwargs)
        if self.context.get('topic_id') is not None:
            discipline = Topic.objects.get(pk=self.context.get('topic_id'))
            aviable_groups = DisciplineAccess.objects.filter(parent_id=discipline.discipline_id).values_list('group_id__name', flat=True)
            disabled_groups = TopicAccess.objects.filter(parent_id=discipline)
            if self.context.get('self_group'):
                disabled_groups = disabled_groups.exclude(group_id=self.context.get('self_group'))

            self.fields['group_id'].queryset = StudentGroupQuide.objects.filter(name__in=aviable_groups) \
                .exclude(name__in=disabled_groups.values_list('group_id__name', flat=True))

class GroupseTopicAccessSerializer(TopicAccessSerializer):
    group_id = StudentGroupQuideSerializer(read_only=True,)

class TopicSerializer(ModelSerializer):
    discipline_id = TopicDisciplineSerializer(read_only=True,)
    topic_video_topic_id = TopicVideoSerializer(read_only=True, many=True)
    topic_material_topic_id = TopicMaterialSerializer(read_only=True, many=True)
    topic_access_parent_id = GroupseTopicAccessSerializer(read_only=True, many=True)
    questions_url = HyperlinkedIdentityField(view_name='teacher_urls:question_api_urls-list',
                                                          lookup_field='pk',
                                                          lookup_url_kwarg='topic_id', read_only=True)

    class Meta:
        model = Topic
        fields = ['pk', 'creation_date', 'title', 'description', 'status', 'discipline_id', 'get_quiz_questions',
                  'questions_url', 'topic_video_topic_id', 'topic_material_topic_id', 'topic_access_parent_id',]

class AnswerHyperLinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        if obj.question_id.variants_type in ['Тест один правильный ответ','Тест несколько правильных ответов',]:
            return self.reverse('teacher_urls:answer_api_urls-detail', kwargs={
                'topic_id': self.context['topic_id'], 'question_id': obj.question_id.pk, 'pk': obj.pk,
            }, format=format, request=request)

        elif obj.question_id.variants_type == 'Тест на последовательность':
            return self.reverse('teacher_urls:answer_sequence_api_urls-detail', kwargs={
                'topic_id': self.context['topic_id'], 'question_id': obj.question_id.pk, 'pk': obj.pk,
            }, format=format, request=request)

        elif obj.question_id.variants_type == 'Тест на соответствие':
            if obj.first_columnn != 0:
                return self.reverse('teacher_urls:answer_compliance_fc_api_urls-detail', kwargs={
                'topic_id': self.context['topic_id'], 'question_id': obj.question_id.pk, 'pk': obj.pk,
                }, format=format, request=request)
            else:
                return self.reverse('teacher_urls:answer_compliance_sc_api_urls-detail', kwargs={
                    'topic_id': self.context['topic_id'], 'question_id': obj.question_id.pk, 'pk': obj.pk,
                }, format=format, request=request)

class AnswerSerializer(ModelSerializer):
    answer_detail = AnswerHyperLinkedIdentityField(view_name='teacher_urls:question_api_urls-detail',)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['topic_access', ]

class QuestionHyperLinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None
        return self.reverse(view_name, kwargs={
            'pk': obj.pk, 'topic_id': self.context['topic_id'],
        }, format=format, request=request)

class QuestionSerializer(ModelSerializer):
    answer_question_id = AnswerSerializer(read_only=True, many=True)
    questions_copy_url = HyperlinkedIdentityField(view_name='teacher_urls:questions_copy',
                                                          lookup_field='pk',
                                                          lookup_url_kwarg='topic_id', read_only=True)
    question_detail = QuestionHyperLinkedIdentityField(view_name='teacher_urls:question_api_urls-detail',)

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

class ReportCardHyperLinkedIdentityField(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        rezult = self.context['all_users_rezults'].filter(user__pk=obj.pk).first()

        if not rezult:
            return None

        if self.context['instance'] == TopicAccess:
            view_name = 'teacher_urls:report_topic_detail'
        return self.reverse(view_name, kwargs={
            'pk': rezult.pk,
        }, format=format, request=request)

class ReportCardSerializer(ModelSerializer):
    rezult_string = SerializerMethodField()
    rezult_detail_url = ReportCardHyperLinkedIdentityField(view_name='teacher_urls:report_decepline_detail',)

    class Meta:
        model = Student
        fields = ['pk', 'first_name', 'last_name', 'patronymic', 'rezult_string', 'rezult_detail_url', ]

    def get_rezult_string(self, obj):
        rezult = self.context['all_users_rezults'].filter(user__pk=obj.pk).first()
        rezult_string = 'N/A'
        if rezult:
            rezult_string = 'testing was started at ' + str(rezult.quize_started_it) +' estimation ' + str(rezult.get_estimation())
            rezult_string = rezult_string + ' correct answers ' + str(rezult.get_correct_answers())
            rezult_string = rezult_string + ' percent ' + str(rezult.get_correct_answers_percent())

        return rezult_string

class ReportCardDetailSerializer(ModelSerializer):

    class Meta:
        model = None
        fields = '__all__'