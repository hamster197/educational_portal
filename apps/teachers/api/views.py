#from django.http import Http404
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.educational_materials.models import Discipline, Topic, DisciplineAccess, TopicAccess, Question, TopicVideo, \
    TopicMaterial, Answer
from apps.portal.api.views import BlogViewSetPagination
from apps.teachers.api.mixins import IsTeacher
from apps.teachers.api.serializers import DisciplineSerializer, TopicSerializer, MainDisciplineAccessSerialser, \
    TopicAccessSerializer, QuestionSerializer, TopicVideoSerializer, TopicMaterialSerializer, QuestionCopySerializer, \
    AnswerEditSerializer, AnswerSequenceEditSerializer, AnswerSecondColumnComplianceSerializer, \
    AnswerComplianceSerializer
from apps.teachers.core import questions_copy_core
from apps.teachers.filters import QuestionFilter
from core.models import Teacher


class AllMethodsMixin(object):
    permission_classes = (IsTeacher,)
    pagination_class = BlogViewSetPagination
class MethodsMixin(object):
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']


class DisciplineViewSet(MethodsMixin):
    serializer_class = DisciplineSerializer

    def get_serializer_context(self):
        context = super(DisciplineViewSet, self).get_serializer_context()
        self_queryset = Discipline.objects.filter(department_id=get_object_or_404(Teacher,
                                                                   username=self.request.user.username).deaprtment_id)
        context.update({'self_queryset': self_queryset})
        return context

class DisciplinePublishedViewSet(DisciplineViewSet, ModelViewSet):
    """
            Перечисляет и редактирует опубликованые Дисциплины.
            permissions:
            IsTeacher
    """
    def get_queryset(self):
        queryset = self.get_serializer_context().get('self_queryset').filter(status=True, )
        return queryset

class DisciplineUnPublishedViewSet(DisciplineViewSet, ModelViewSet):
    """
            Перечисляет и редактирует неопубликованые Дисциплины.
            permissions:
            IsTeacher
    """
    def get_queryset(self):
        queryset = self.get_serializer_context().get('self_queryset').filter(status=False,)
        return queryset

class DisciplineAccessViewSet(MethodsMixin, ModelViewSet):
    """
            редактирует Доступы к дисциплинам.
            permissions:
            IsTeacher
    """
    serializer_class = MainDisciplineAccessSerialser

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["discipline_id"] = self.kwargs['discipline_id']
        return context

    def get_queryset(self):
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = DisciplineAccess.objects.filter(parent_id__department_id=department_id,
                                                   parent_id__id=self.kwargs['discipline_id'])
        return queryset

    def perform_create(self, serializer):
        if not Discipline.objects.filter(id=self.kwargs['discipline_id']).exists():
            raise Http404
        discipline_id = Discipline.objects.get(id=self.kwargs['discipline_id'])
        user_department = Teacher.objects.get(id=self.request.user.pk).deaprtment_id
        if discipline_id.department_id == user_department:
            try:
                serializer.save(parent_id_id=self.kwargs['discipline_id'])
            except:
                raise ValidationError('Valudation error.')
        else:
            raise PermissionDenied({"message": "You don't have permission to access",})

    def perform_update(self, serializer):
        try:
            serializer.save(data=self.request.data)
        except:
            raise ValidationError('Valudation error.')
class TopicViewSet(MethodsMixin, ModelViewSet):
    """
            Перечисляет и создает, редактирует Темы.
            permissions:
            IsTeacher
    """
    serializer_class = TopicSerializer

    def get_queryset(self):
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = Topic.objects.filter(discipline_id__department_id=department_id, discipline_id__id=self.kwargs['discipline_id'])
        return queryset

    def perform_create(self, serializer):
        if not Discipline.objects.filter(id=self.kwargs['discipline_id']).exists():
            raise Http404
        discipline_id = Discipline.objects.get(id=self.kwargs['discipline_id'])
        user_department = Teacher.objects.get(id=self.request.user.pk).deaprtment_id
        if discipline_id.department_id == user_department:
            serializer.save(discipline_id=discipline_id)
        else:
            raise PermissionDenied({"message": "You don't have permission to access",})

class TopicVideoViewSet(AllMethodsMixin, ModelViewSet):
    """
            Перечисляет и создает, редактирует Видео в Темах.
            permissions:
            IsTeacher
    """
    serializer_class = TopicVideoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return TopicVideo.objects.none()
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = TopicVideo.objects.filter(topic_id__discipline_id__department_id=department_id, \
                                             topic_id__id=self.kwargs['topic_id'])
        return queryset

    def perform_create(self, serializer):
        if not Topic.objects.filter(id=self.kwargs['topic_id']).exists():
            raise Http404
        topic_id = Topic.objects.get(id=self.kwargs['topic_id'])
        user_department = Teacher.objects.get(id=self.request.user.pk).deaprtment_id
        if topic_id.discipline_id.department_id == user_department:
            serializer.save(topic_id=topic_id)
        else:
            raise PermissionDenied({"message": "You don't have permission to access",})

class TopicMaterialViewSet(TopicVideoViewSet):#AllMethodsMixin, ModelViewSet
    """
            Перечисляет и создает, редактирует Видео в Темах.
            permissions:
            IsTeacher
    """
    serializer_class = TopicMaterialSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return TopicMaterial.objects.none()
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = TopicMaterial.objects.filter(topic_id__discipline_id__department_id=department_id, \
                                             topic_id__id=self.kwargs['topic_id'])
        return queryset

class TopicAccessViewSet(MethodsMixin, ModelViewSet):
    """
            редактирует Доступы к темам.
            permissions:
            IsTeacher
    """
    serializer_class = TopicAccessSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["topic_id"] = self.kwargs['topic_id']
        return context

    def get_queryset(self,):
        if getattr(self, "swagger_fake_view", False):
            return TopicAccess.objects.none()
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = TopicAccess.objects.filter(parent_id__discipline_id__department_id=department_id,
                                              parent_id__id=self.kwargs['topic_id'])
        return queryset

    def perform_create(self, serializer):
        if not Topic.objects.filter(id=self.kwargs['topic_id']).exists():
            raise Http404
        topic = Topic.objects.get(id=self.kwargs['topic_id'])
        user_department = Teacher.objects.get(id=self.request.user.pk).deaprtment_id
        if topic.discipline_id.department_id == user_department:
            try:
                serializer.save(parent_id=topic)
            except:
                raise ValidationError('Valudation error',)
        else:
            raise PermissionDenied({"message": "You don't have permission to access",})

    def perform_update(self, serializer):
        try:
            serializer.save(data=self.request.data)
        except:
            raise ValidationError('Valudation error')

class QuestionViewSet(MethodsMixin, ModelViewSet):
    """
            отображает, редактирует и создает вопросы к темам.
            permissions:
            IsTeacher

    """
    serializer_class = QuestionSerializer
    filterset_class = QuestionFilter

    def get_queryset(self,):
        if getattr(self, "swagger_fake_view", False):
            return Question.objects.none()
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        queryset = Question.objects.filter(topic_access=self.kwargs['topic_id'],
                                           topic_access__discipline_id__department_id=department_id,)
        return queryset

    def perform_create(self, serializer):
        if not Topic.objects.filter(id=self.kwargs['topic_id']).exists():
            raise Http404
        topic = Topic.objects.get(id=self.kwargs['topic_id'])
        user_department = Teacher.objects.get(id=self.request.user.pk).deaprtment_id
        if topic.discipline_id.department_id == user_department:
            try:
                question = serializer.save()
                question.topic_access.add(topic)
            except:
                raise ValidationError('Valudation error',)
        else:
            raise PermissionDenied({"message": "You don't have permission to access",})

class QuestionCopy(AllMethodsMixin, APIView):
    """
             копирует вопросы в тему.
            permissions:
            IsTeacher
    """
    serializer_class = QuestionCopySerializer
    http_method_names = ['post', ]

    def post(self, request, **kwargs):
        user = Teacher.objects.get(pk=self.request.user.pk)
        topic_from = Topic.objects.get(pk=kwargs['topic_id'])
        if user.deaprtment_id != topic_from.discipline_id.department_id:
            raise Http404
        serializer = QuestionCopySerializer(data=request.data, context={'request': request})
        error = ''
        action = ''
        if serializer.is_valid():
            topic_to_copy = serializer.data['topic_to']
            action += 'В тему ' + str(topic_to_copy) + '(' + str(topic_to_copy.pk) + ')'
        else:
            error = str(serializer.errors)
        from rest_framework.response import Response
        return Response(str(questions_copy_core(topic_from, topic_to_copy, user)) + ' questions was copied ' + error)



class AnswerObjectMixin(AllMethodsMixin, ModelViewSet):

    def check_permissions(self, request):
        if not Topic.objects.filter(pk=self.kwargs['topic_id']).exists() \
                or not Question.objects.filter(pk=self.kwargs['question_id'],
                                               variants_type__in=self.question_type).exists():
            raise Http404
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        if department_id != Topic.objects.get(pk=self.kwargs['topic_id']).discipline_id.department_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('HTTP 403 Forbidden')

    def get_queryset(self,):

        queryset = Answer.objects.filter(question_id__topic_access__id=self.kwargs['topic_id'],#question_id__topic_access=topic,
                                         question_id=self.kwargs['question_id'], question_id__variants_type__in=self.question_type)

        return queryset.order_by('-pk')

class AnswerViewSet(AnswerObjectMixin):

    """
            редактирует, удаляет и добавляет тексты ответов к вопросам.
            permissions:
            IsTeacher
            'Тест один правильный ответ', 'Тест несколько правильных ответов',

    """
    serializer_class = AnswerEditSerializer
    question_type = ['Тест один правильный ответ', 'Тест несколько правильных ответов',]



    def perform_create(self, serializer):
        try:
            serializer.save(question_id=self.get_queryset().first().question_id)
        except:
            raise ValidationError('Valudation error', )

class AnswerSequenceViewSet(AnswerObjectMixin):

    """
            редактирует, удаляет и добавляет тексты ответов к вопросам.
            permissions:
            IsTeacher
            'Тест на последовательность',
    """
    serializer_class = AnswerSequenceEditSerializer
    question_type = ['Тест на последовательность', ]


    def perform_create(self, serializer):
        try:
            serializer.save(question_id=self.get_queryset().first().question_id,
                                first_columnn=self.get_queryset().count() + 1)
        except:
            raise ValidationError('Valudation error', )

#############################
## Add and check for delete aswers
#############################
class AnswerFirstColumnComplianceViewSet(AnswerObjectMixin):
    """
            редактирует, удаляет и добавляет тексты ответов к вопросам.
            permissions:
            IsTeacher
            'Тест на соответствие'(первый столбец),

    """
    serializer_class = AnswerSequenceEditSerializer
    question_type = ['Тест на соответствие', ]
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace', 'delete',]

    def filter_queryset(self, queryset):
        return self.get_queryset().filter(second_column=0).order_by('first_columnn')

class AnswerSecondColumnComplianceViewSet(AnswerFirstColumnComplianceViewSet):
    """
            редактирует, удаляет и добавляет тексты ответов к вопросам.
            permissions:
            IsTeacher
            'Тест на соответствие'(второй столбец),

    """
    serializer_class = AnswerSecondColumnComplianceSerializer

    def filter_queryset(self, queryset):
        return self.get_queryset().filter(first_columnn=0).order_by('second_column')

    def perform_destroy(self, instance):
        from django.db.models import Q
        Answer.objects.filter(Q(first_columnn=instance.second_column) | Q(second_column=instance.second_column),
                              question_id__id=self.kwargs['question_id'],).delete()

class AnswerComplianceNew(AllMethodsMixin, APIView):
    """
             копирует вопросы в тему.
            permissions:
            IsTeacher
    """
    serializer_class = AnswerComplianceSerializer
    http_method_names = ['post',]

    def post(self, request, **kwargs):
        user = Teacher.objects.get(pk=self.request.user.pk)
        topic_from = Topic.objects.get(pk=kwargs['topic_id'])
        if user.deaprtment_id != topic_from.discipline_id.department_id:
            raise Http404
        serializer = AnswerComplianceSerializer(data=request.data, context={'request': request})
        action = ''
        error = ''
        if serializer.is_valid():
            position = Answer.objects.filter(question_id=self.kwargs['question_id'], first_columnn=0).count() + 1
            Answer.objects.create(question_id_id=self.kwargs['question_id'], first_columnn=position,
                                  ansr_text=serializer.data['question'])
            Answer.objects.create(question_id_id=self.kwargs['question_id'], second_column=position,
                                  ansr_text=serializer.data['answer'])
            action += 'Instance was added'
        else:
            error = str(serializer.errors)
        from rest_framework.response import Response
        return Response(action + error)





