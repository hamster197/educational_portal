from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Student, Teacher

from django.db import transaction

def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner

@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
def update_student_user_group(sender, instance, **kwargs):
    if 'Student' in str(sender):
        new_group, created = Group.objects.get_or_create(name='students')
        if instance.active_group_id:
            if not instance.active_group_id in instance.all_group_id.all():
                instance.all_group_id.add(instance.active_group_id)
    if 'Teacher' in str(sender):
        new_group, created = Group.objects.get_or_create(name='teachers')
        if instance.deaprtment_id:
            if not instance.deaprtment_id in instance.all_department_id.all():
                instance.all_department_id.add(instance.deaprtment_id)
    if not instance.groups == new_group:
        instance.groups.add(new_group)
