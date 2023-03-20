from django.db import models

from apps.educational_materials.models import Discipline
from core.models import MainUser


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