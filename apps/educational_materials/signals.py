from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from apps.educational_materials.models import *
from apps.journals.models import DisciplineJournal
from core.core import get_user_from_request
from core.models import Teacher, DepartmentQuide

@receiver(pre_save, sender=Discipline)
@receiver(pre_save, sender=Topic)
def change_discipline_theme_status(sender, instance, **kwargs):
    if instance.id is not None:
        if 'Discipline' in str(sender):
            previous = Discipline.objects.get(id=instance.id)
        elif 'Topic' in str(sender):
            previous = Topic.objects.get(id=instance.id)
        if previous.status != instance.status:
            discpline = instance.title + ' (' + str(instance.pk) + ' )'
            log_string = ' status was changed from ' + str(previous.status) + ' to ' + str(instance.status)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'

            if 'Discipline' in str(sender):
                DisciplineJournal.objects.create(action=log_string, title=discpline,
                                                 material_type='Дисциплинa')
            if 'Topic' in str(sender):
                DisciplineJournal.objects.create(action=log_string, title=discpline,
                                                 material_type='Tемa')


@receiver(post_save, sender=Discipline)
@receiver(post_save, sender=Topic)
def update_discipline(sender, instance,  created, **kwargs, ):

    if created:
        discpline = instance.title + ' (' + str(instance.pk) + ' )'
        log_string = 'created ' + discpline
        log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'

        if 'Discipline' in str(sender):
            DisciplineJournal.objects.create(action=log_string, title=discpline,
                                             material_type='Дисциплинa')
        elif 'Topic' in str(sender):
            DisciplineJournal.objects.create(action=log_string, title=discpline,
                                             material_type='Tемa')

    if 'Discipline' in str(sender):
        if Teacher.objects.filter(username=get_user_from_request()).exists():
            department_id = get_object_or_404(Teacher, username=get_user_from_request()).deaprtment_id
        else:
            department_id, created = DepartmentQuide.objects.get_or_create(name='N/A', faculty_id_id=1)

        if instance.department_id != department_id:
            if instance.department_id is not None:
                log_string = 'Кафедра was changed from ' + str(instance.department_id) + ' to ' + str(department_id)
                log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
                discpline = instance.title + ' (' + str(instance.pk) + ' )'
                DisciplineJournal.objects.create(action=log_string, title=discpline)

            instance.department_id = department_id
            instance.save()

@receiver(post_save, sender=DisciplineAccess)
@receiver(post_save, sender=TopicAccess)
def create_parent_access(sender, instance,  created, **kwargs, ):

    if created:
        log_string = ' created ' + str(instance) + ' id=' + str(instance.pk)
        log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'

        if 'DisciplineAccess' in str(sender):
            DisciplineJournal.objects.create(action=log_string, title=instance,
                                             material_type='Доступ к Дисциплине(и Тестам)')
        elif 'TopicAccess' in str(sender):
            DisciplineJournal.objects.create(action=log_string, title=instance,
                                             material_type='Доступ к Теме(и Тестам)')

@receiver(pre_save, sender=DisciplineAccess)
@receiver(pre_save, sender=TopicAccess)
def change_parent_date(sender, instance, **kwargs):
    if instance.id is not None:
        log_string = ''
        if 'DisciplineAccess' in str(sender):
            previous = DisciplineAccess.objects.get(id=instance.id)
        elif 'TopicAccess' in str(sender):
            previous = TopicAccess.objects.get(id=instance.id)

        if previous.discipline_access_start != instance.discipline_access_start:
            log_string = ' discipline_access_start was changed from ' + str(previous.discipline_access_start) + \
                         ' to ' + str(instance.discipline_access_start)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
        if previous.discipline_access_end != instance.discipline_access_end:
            log_string = ' discipline_access_end was changed from ' + str(previous.discipline_access_end) + \
                         ' to ' + str(instance.discipline_access_end)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
        if previous.test_quize_start != instance.test_quize_start:
            log_string = ' test_quize_start was changed from ' + str(previous.test_quize_start) + \
                         ' to ' + str(instance.test_quize_start)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
        if previous.test_quize_end != instance.test_quize_end:
            log_string = ' test_quize_end was changed from ' + str(previous.test_quize_end) + \
                         ' to ' + str(instance.test_quize_end)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
        if previous.final_quize_start != instance.final_quize_start:
            log_string = ' final_quize_start was changed from ' + str(previous.final_quize_start) + \
                         ' to ' + str(instance.final_quize_start)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'
        if previous.final_quize_end != instance.final_quize_end:
            log_string = ' final_quize_end was changed from ' + str(previous.final_quize_end) + \
                         ' to ' + str(instance.final_quize_end)
            log_string += ' by ' + str(get_user_from_request().username) + ' (' + str(get_user_from_request().pk) + ' )'

        if log_string:
            if 'DisciplineAccess' in str(sender):
                DisciplineJournal.objects.create(action=log_string, title=instance,
                                                 material_type='Доступ к Дисциплине(и Тестам)')
            elif 'TopicAccess' in str(sender):
                DisciplineJournal.objects.create(action=log_string, title=instance,
                                                 material_type='Доступ к Теме(и Тестам)')


@receiver(post_delete, sender=Answer)
def delete_answer(sender, instance, **kwargs, ):
    if instance.question_id.variants_type == 'Тест на последовательность':
        counter = 0
        for answer in instance.question_id.answer_question_id.all().order_by('first_columnn'):
            counter += 1
            answer.first_columnn = counter
            answer.save()

    if instance.question_id.variants_type == 'Тест на соответствие':
        answers = instance.question_id.answer_question_id.all()
        counter = 0
        for answer in answers.filter(second_column=0).order_by('first_columnn'):
            counter += 1
            answer.first_columnn = counter
            answer.save()

        counter = 0
        for answer in answers.filter(first_columnn=0).order_by('second_column'):
            counter += 1
            answer.second_column = counter
            answer.save()

@receiver(pre_save, sender=Answer)
def change_column_answer(sender, instance, **kwargs):
    if instance.id is not None:
        previous = Answer.objects.get(id=instance.id)
        if previous.first_columnn != instance.first_columnn:
            Answer.objects.filter(question_id=previous.question_id, first_columnn=instance.first_columnn). \
                    update(first_columnn=previous.first_columnn)
        if previous.second_column != instance.second_column:
            Answer.objects.filter(question_id=previous.question_id, second_column=instance.second_column). \
                    update(second_column=previous.second_column)

