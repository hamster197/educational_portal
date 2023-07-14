import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone


from apps.educational_materials.models import DisciplineAccess, TopicAccess, Question
from apps.journals.models import QuizeLogDeciplineJournal, QuizeLogTopicJournal
from apps.students.models import QuizeRezultDecepline, QuizeRezultTopic
from core.models import Student

def get_student_group(self):
    if Student.objects.filter(pk=self.request.user.pk).exists():
        return get_object_or_404(Student, pk=self.request.user.pk).active_group_id
    else:
        return None


def get_student_aviable_materials(self, instance):
    return instance.objects.filter(group_id=get_student_group(self),
                                           discipline_access_end__gte=timezone.now(),
                                           discipline_access_start__lte=timezone.now(),
                                           parent_id__status=True, )

def get_student_unaviable_diciplines(self):
    return DisciplineAccess.objects.filter(group_id=get_student_group(self),
                                           discipline_access_end__lte=timezone.now(),
                                           parent_id__status=True, )

def get_for_aviable_quize_access(self, ):

    request_group = get_student_group(self)
    queryset = self.model.objects.filter(Q(test_quize_start__lte=self.now, test_quize_end__gte=self.now)
                                         |Q(final_quize_start__lte=self.now, final_quize_end__gte=self.now),
                                         parent_id__status=True, group_id=request_group, )

    if self.model == TopicAccess:
        queryset = queryset.filter(parent_id__discipline_id__status=True, )
    return queryset

def check_for_aviable_quize_rezult(self,):

    if self.model == DisciplineAccess:
        rezults_type = QuizeRezultDecepline
    elif self.model == TopicAccess:
        rezults_type = QuizeRezultTopic

    rezults = rezults_type.objects.filter(user=self.request.user, parent_id=self.get_object(), ended_quize=True)
    if rezults.exists():
        if self.quize_status:
            rezults = rezults.filter(final_quize=True).first()
        else:
            rezults = rezults.filter(final_quize=False).first()
    else:
        rezults = None

    return rezults

def get_random_question(self):
    if self.model == DisciplineAccess:
        answered_questions = QuizeLogDeciplineJournal.objects.filter(parent_id=self.get_object().pk,
                                                                 user_id=self.request.user.pk).values_list(
            'question_id', flat=True)
        topics = self.get_object().parent_id.topic_discipline_id.filter(status=True)
        random_question = Question.objects.filter(topic_access__in=topics, ).order_by('?')\
            .exclude(pk__in=list(answered_questions)).first()
    elif self.model == TopicAccess:
        answered_questions = QuizeLogTopicJournal.objects.filter(parent_id=self.get_object().pk,
                                                                 user_id=self.request.user.pk).values_list(
            'question_id', flat=True)
        random_question = Question.objects.filter(topic_access=self.get_object().parent_id,
                                                  topic_access__status=True).exclude(pk__in=list(answered_questions))\
            .order_by('?').first()

    return random_question

def get_or_create_for_aviable_quize_rezult(self,):
    if self.model == DisciplineAccess:
        rezults_type = QuizeRezultDecepline
        journal = QuizeLogDeciplineJournal
    elif self.model == TopicAccess:
        rezults_type = QuizeRezultTopic
        journal = QuizeLogTopicJournal
    rezult, status = rezults_type.objects.get_or_create(user=Student.objects.get(pk=self.request.user.pk),
                                                 parent_id=self.get_object(),)

    if rezult.final_quize != self.quize_status or status:
        rezult.final_quize = self.quize_status
        rezult.quize_started_it = datetime.datetime.now()
        rezult.ended_quize = False
        journal.objects.filter(parent_id=self.get_object().pk, user_id=self.request.user.pk).delete()
        rezult.current_question = get_random_question(self)
        rezult.save()

    return rezult

def get_timer(self,):
    now = datetime.datetime.now()
    quize_started = get_or_create_for_aviable_quize_rezult(self,).quize_started_it
    delta = now.replace(tzinfo=None) - quize_started.replace(tzinfo=None)
    timer_seconds = self.get_object().time * 60 - delta.seconds
    return timer_seconds

def get_aviable_questions(self):
    status = True
    if self.model == DisciplineAccess:
        journal = QuizeLogDeciplineJournal
    elif self.model == TopicAccess:
        journal = QuizeLogTopicJournal
    if self.get_object().quiestion_quantity <= journal.objects.filter(parent_id=self.get_object().pk,
                                                                      user_id=self.request.user.pk).count():
        status = False

    return status

def get_quize_rezult(self):

    if self.model == DisciplineAccess:
        queryset = get_for_aviable_quize_access(self, ).filter(
            quize_declpline_rezult_discipline_id__user=self.request.user, )
    elif self.model == TopicAccess:
        queryset = get_for_aviable_quize_access(self, ).filter(
            quize_topic_rezult_topic_id__user=self.request.user, )

    return queryset




