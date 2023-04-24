from apps.educational_materials.models import Question, DisciplineAccess, TopicAccess
from apps.journals.models import QuestionsCopyJournal
from core.models import Teacher


def questions_copy_core(topic_from, topic_to_copy, author):
    counter = 0
    action = ''
    QstTopicRelation = Question.topic_access.through
    instances = []
    queryset = Question.objects.filter(topic_access=topic_from).exclude(topic_access=topic_to_copy)
    if queryset.exists():
        for question in queryset:
            instances.append(QstTopicRelation(question=question, topic=topic_to_copy))
            counter += 1
            action += ' ' + str(question.pk)
        QstTopicRelation.objects.bulk_create(instances)
        action += ' В тему ' + str(topic_to_copy) + '(' + str(topic_to_copy.pk) + ')'
        QuestionsCopyJournal.objects.create(action=action, author=author.username + ' id=' + str(author.pk),
                                            from_theme=str(topic_from) + '(' + str(topic_from.pk) + ')')
    return counter

def get_report_card_queryset(self):
    deaprtment_id = Teacher.objects.get(pk=self.request.user.pk).deaprtment_id
    if self.model == DisciplineAccess:
        queryset = self.model.objects.filter(parent_id__department_id=deaprtment_id)
    elif self.model == TopicAccess:
        queryset = self.model.objects.filter(parent_id__discipline_id__department_id=deaprtment_id)
    return queryset

def get_final_quize_status(self):
    from django.utils import timezone
    final_quize_status = False
    if self.object.final_quize_start <= timezone.now() and self.object.final_quize_end >= timezone.now():
        final_quize_status = True
    return final_quize_status