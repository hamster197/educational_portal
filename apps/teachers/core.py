from apps.educational_materials.models import Question
from apps.journals.models import QuestionsCopyJournal


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

