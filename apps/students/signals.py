from django.db.models.signals import pre_delete#post_delete,
from django.dispatch import receiver

from apps.journals.models import QuizeLogDeciplineJournal, QuizeLogTopicJournal, QuizeLogRetakeDeciplineJournal, \
    QuizeLogRetakeTopicJournal
from apps.students.models import QuizeRezultDecepline, QuizeRezultTopic
from core.core import get_user_from_request

@receiver(pre_delete, sender=QuizeRezultDecepline)
@receiver(pre_delete, sender=QuizeRezultTopic)
def retake_quize(sender, instance, **kwargs, ):
    ## async send mail?
    if sender == QuizeRezultDecepline:
        logs_to_delete = QuizeLogDeciplineJournal
        journal = QuizeLogRetakeDeciplineJournal
    elif sender == QuizeRezultTopic:
        logs_to_delete = QuizeLogTopicJournal
        journal = QuizeLogRetakeTopicJournal

    logs_to_delete.objects.filter(parent_id=instance.parent_id.pk, user_id=instance.user.pk).delete()
    student_full_name = instance.user.first_name + ' ' + instance.user.last_name
    user_full_name = get_user_from_request().first_name + ' ' + get_user_from_request().last_name
    journal.objects.create(student_id=instance.user.pk, student_full_name=student_full_name,
                           user_id=str(get_user_from_request().pk), user_full_name=user_full_name,
                           parent_id=instance.pk, )
