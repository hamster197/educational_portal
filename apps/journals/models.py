from django.db import models

from apps.educational_materials.models import Discipline, DisciplineAccess, TopicAccess
from core.models import MainUser, Student

#Create your models here.
material_type_choises = (('Tемa','Tемa'),('Дисциплинa','Дисциплинa'),
                         ('Доступ к Дисциплине(и Тестам)','Доступ к Дисциплине(и Тестам)'),
                         ('Доступ к Теме(и Тестам)','Доступ к Теме(и Тестам)'))

class DisciplineJournal(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    material_type = models.CharField('Типа учебного материала', choices=material_type_choises, max_length=45,)
    title = models.CharField('title, id', max_length=250)
    action = models.CharField('Действие', max_length=5000)

    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал редактирования Дисциплин и Тем'
        verbose_name_plural = 'Журнал редактирования Дисциплин и Тем'

class QuestionsCopyJournal(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True, )
    action = models.CharField('Действие(скопированно вопросов)', max_length=5000)
    author = models.CharField('Автор', max_length=200)
    from_theme = models.CharField('Из темы', max_length=5000)

    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал копирования Вопросов'
        verbose_name_plural = 'Журнал копирования Вопросов'

class QuizeLogObject(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now=True)
    question_id = models.PositiveIntegerField('Вопрос(pk)', )
    user_id = models.PositiveIntegerField('Студент(pk)', )
    user_full_name = models.CharField('Студент', max_length=155)
    answer_right = models.BooleanField('Ответ верен?', default=False)
    test_type = models.BooleanField('Итоговый тест??', default=False)
    image = models.ImageField('Photo', upload_to='quize_log/%Y/%m/%d/', blank=True)

    class Meta:
        app_label = 'journals'
        abstract = True

class QuizeLogDeciplineJournal(QuizeLogObject):
    parent_id = models.PositiveIntegerField('Дисциплинa(Доступы групп)(pk)',)
    parent_name = models.CharField('Дисциплинa(Доступы групп)', max_length=255)

    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал сдачи тестов Дисциплин'
        verbose_name_plural = 'Журнал сдачи тестов Дисциплин'

class QuizeLogTopicJournal(QuizeLogObject):
    parent_id = models.PositiveIntegerField('Тема(Доступы групп)(pk)', )
    parent_name = models.CharField('Тема(Доступы групп)', max_length=255)


    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал сдачи тестов Тем'
        verbose_name_plural = 'Журнал сдачи тестов Тем'

##retake quize
class QuizeRetakeLogObject(models.Model):
    creation_date = models.DateTimeField('Дата создания', auto_now=True)
    student_id = models.PositiveIntegerField('Студент(pk)', null=True)
    student_full_name = models.CharField('Студент', max_length=155, blank=True)
    user_id = models.PositiveIntegerField('User(pk)', )
    user_full_name = models.CharField('User', max_length=155)

class QuizeLogRetakeDeciplineJournal(QuizeRetakeLogObject):
    parent_id = models.PositiveIntegerField('Дисциплинa(Доступы групп)(pk)',)

    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал  пересдачи тестов Дисциплин'
        verbose_name_plural = 'Журнал пересдачи тестов Дисциплин'

class QuizeLogRetakeTopicJournal(QuizeRetakeLogObject):
    parent_id = models.PositiveIntegerField('Тема(Доступы групп)(pk)', )

    class Meta:
        app_label = 'journals'
        verbose_name = 'Журнал пересдачи тестов Тем'
        verbose_name_plural = 'Журнал пересдачи тестов Тем'