from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
import calendar

from django.utils import timezone

from core.models import StudentGroupQuide, Teacher


# Create your models here.


class Discipline(models.Model):
    department_id = models.ForeignKey('core.DepartmentQuide', verbose_name='Кафедра:', on_delete=models.CASCADE,
                                      related_name='discipline_department_id', null=True, )
    creation_date = models.DateTimeField(verbose_name='Дата создания:', auto_now=True, )
    title = models.CharField(verbose_name='Название дисциплины:', max_length=255, blank=False, unique=True)
    description = RichTextUploadingField(verbose_name='Описание дисциплины:', blank=False, )
    program = RichTextUploadingField(verbose_name='Программа дисциплины:', blank=False, )
    status = models.BooleanField(verbose_name='Опубликован?', max_length=15, default=False, )

    class Meta:
        verbose_name = 'Дисциплинa'
        verbose_name_plural = 'Дисциплины'
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_quiz_questions(self):
        return Question.objects.filter(topic_access__discipline_id=self).count()

    def get_themes(self):
        return Topic.objects.filter(discipline_id=self).count()

class Topic(models.Model):
    discipline_id = models.ForeignKey(Discipline, verbose_name='Дисциплинa:', on_delete=models.CASCADE,
                                      related_name='topic_discipline_id', )
    creation_date = models.DateTimeField(verbose_name='Дата создания:', auto_now=True, )
    title = models.CharField(verbose_name='Название темы:', max_length=255, blank=False, unique=True)
    description = RichTextUploadingField(verbose_name='Текст темы', blank=True, )
    status = models.BooleanField(verbose_name='Опубликован?', default=False, )

    class Meta:
        verbose_name = 'Tема'
        verbose_name_plural = 'Tемы'
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_quiz_questions(self):
        return Question.objects.filter(topic_access=self).count()

class TopicVideo(models.Model):
    topic_id = models.ForeignKey(Topic, verbose_name='Название Tемы', on_delete=models.CASCADE,
                                  related_name='topic_video_topic_id',)
    title = models.CharField(verbose_name='Название Видео',  max_length=155, blank=False)
    video = models.FileField(verbose_name='Видео', upload_to='materials/video/%Y/%m/%d/', blank=True)
    video_link = models.URLField(verbose_name='Видео(Линк)',  blank=True)

    class Meta:
        verbose_name = 'Tемы (Видео)'
        verbose_name_plural = 'Tемa(Видео)'
        ordering = ['-pk']

    def __str__(self):
        return self.title

class TopicMaterial(models.Model):
    topic_id = models.ForeignKey(Topic, verbose_name='Название Tемы', on_delete=models.CASCADE,
                                  related_name='topic_material_topic_id',)
    title = models.CharField(verbose_name='Название материал Tемы',  max_length=155, blank=True, )
    topic_material = models.FileField(verbose_name='Mатериал Tемы', upload_to='materials/material/%Y/%m/%d/',
                                        blank=False, )
    class Meta:
        verbose_name = 'Tемы (материалы Tемы)'
        verbose_name_plural = 'Tемa (материалы Tемa)'
        ordering = ['-pk']

    def __str__(self):
        return self.title



class ParentAccess(models.Model):
    discipline_access_start = models.DateTimeField(verbose_name='Дата начала доступа к материалу(Дисплины или Темы):',
                                                    default=timezone.now)

    discipline_access_end = models.DateTimeField(verbose_name='Дата окончания доступа  к материалу(Дисплины или Темы):',
                                                  default=timezone.now().replace(day=
                                                  calendar.monthrange(timezone.now().year, 12)[1],
                                                                                month=12))

    quiestion_quantity = models.IntegerField('Kоличество вопросов в тесте ', validators=[MinValueValidator(0)], default=0,)
    time = models.IntegerField(verbose_name='Время сдачи тестов(в минутах)', default=10,
                               validators=[MinValueValidator(5)],)

    test_quize_start = models.DateTimeField(verbose_name='Дата начала тренировочного теста:',
                                                    default=timezone.now)

    test_quize_end = models.DateTimeField(verbose_name='Дата окончания тренировочного теста:',
                                                  default=timezone.now().replace(day=
                                                  calendar.monthrange(timezone.now().year, 11)[1],
                                                                                month=11))
    final_quize_start = models.DateTimeField(verbose_name='Дата начала итогового теста:',
                                                    default=timezone.now)

    final_quize_end = models.DateTimeField(verbose_name='Дата окончания итогового теста:',
                                                  default=timezone.now().replace(day=
                                                  calendar.monthrange(timezone.now().year, 11)[1],
                                                                                month=11))

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.parent_id) + ' ( ' + str(self.group_id) + ' ) '


    def clean(self):
        errors = {}
        if self.discipline_access_start >= self.discipline_access_end:
            errors['discipline_access_start'] = 'Дата доступа к дисциплине( неправильный промежуток )'
        if self.test_quize_start >= self.test_quize_end:
            errors['test_quize_start'] = 'Дата доступа тренировочного теста( неправильный промежуток )'
        if self.final_quize_start >= self.final_quize_end:
            errors['final_quize_start'] = 'Дата доступа итогового теста( неправильный промежуток )'
        if errors:
            raise ValidationError(errors)


error_string = 'Дата доступа к материалу(Дисплины или Темы) - неправильный промежуток '

class DisciplineAccess(ParentAccess):
    parent_id = models.ForeignKey(Discipline, verbose_name='Дисциплинa:', on_delete=models.CASCADE,
                                      related_name='discipline_access_parent_id', )
    group_id = models.ForeignKey(StudentGroupQuide, verbose_name='Группа:', on_delete=models.CASCADE,
                                      related_name='discipline_access_group_id', null=True)

    def __str__(self):
        return str(self.group_id)

    class Meta:
        verbose_name = 'Дисциплинa(Доступы групп)'
        verbose_name_plural = 'Дисциплины(Доступы групп)'
        unique_together = ['parent_id', 'group_id']
        ordering = ['-pk']

    def save(self, **kwargs):
        self.clean()
        return super(DisciplineAccess, self).save(**kwargs)

    def clean(self):
        errors = {}
        self.validate_unique()
        if self.discipline_access_start > self.test_quize_start:
            errors['test_quize_start'] = error_string
        if self.discipline_access_end < self.test_quize_end:
            errors['test_quize_end'] = error_string
        if self.discipline_access_start > self.final_quize_start:
            errors['final_quize_start'] = error_string
        if self.discipline_access_end < self.final_quize_end:
            errors['final_quize_end'] = error_string
        questions_count = Question.objects.filter(topic_access__in=self.parent_id.topic_discipline_id.all()).count()
        if self.quiestion_quantity > questions_count:
            errors['quiestion_quantity'] = 'Всего вопросов в теме: ' + str(questions_count)
        if errors:
            raise ValidationError(errors)



class TopicAccess(ParentAccess):
    parent_id = models.ForeignKey(Topic, verbose_name='Тема:', on_delete=models.CASCADE,
                                      related_name='topic_access_parent_id', )
    group_id = models.ForeignKey(StudentGroupQuide, verbose_name='Группа:1', on_delete=models.CASCADE,
                                      related_name='topic_access_group_id', null=True)

    def __str__(self):
        return str(self.group_id)

    class Meta:
        verbose_name = 'Тема(Доступы групп)'
        verbose_name_plural = 'Тема(Доступы групп)'
        unique_together = ['parent_id', 'group_id']
        ordering = ['-pk']

    def save(self, **kwargs):
        self.clean()
        return super(TopicAccess, self).save(**kwargs)

    def clean(self):
        errors = {}
        if self.group_id is not None:
            if not DisciplineAccess.objects.filter(parent_id=self.parent_id.discipline_id,
                                                   group_id=self.group_id).exists():
                errors['discipline_access_start'] = 'Добавьте доступ к дисциплине!'
            else:
                descepline_access = DisciplineAccess.objects.get(parent_id=self.parent_id.discipline_id,
                                                                 group_id=self.group_id)
                if self.discipline_access_start < descepline_access.discipline_access_start:
                    errors['discipline_access_start'] = error_string + 'Доступ к дисциплине с ' + str(
                        descepline_access.discipline_access_start)
                if self.discipline_access_end > descepline_access.discipline_access_end:
                    errors['discipline_access_end'] = error_string + 'Доступ к дисциплине по ' + str(
                        descepline_access.discipline_access_end)
                if self.discipline_access_start > self.test_quize_start:
                    errors['test_quize_start'] = error_string + 'Доступ к дисциплине с ' + str(
                        descepline_access.discipline_access_start)
                if self.discipline_access_end < self.test_quize_end:
                    errors['test_quize_end'] = error_string + 'Доступ к дисциплине по ' + str(
                        descepline_access.discipline_access_end)
                if self.discipline_access_start > self.final_quize_start:
                    errors['final_quize_start'] = error_string + 'Доступ к дисциплине с ' + str(
                        descepline_access.discipline_access_start)
                if self.discipline_access_end < self.final_quize_end:
                    errors['final_quize_end'] = error_string + 'Доступ к дисциплине по ' + str(
                        descepline_access.discipline_access_end)
                if self.quiestion_quantity > self.parent_id.question_topic_access_id.all().count():
                    errors['quiestion_quantity'] = 'Всего вопросов в теме: ' \
                                                   + str(self.parent_id.question_topic_access_id.all().count())

        if errors:
            raise ValidationError(errors)

class Question(models.Model):
    topic_access = models.ManyToManyField(Topic, related_name='question_topic_access_id', verbose_name='Доступ к теме:',)
    question_text = RichTextUploadingField(verbose_name='Текст вопроса:', max_length=5000, blank=False)
    image = models.ImageField(verbose_name='Фото:', upload_to='image/quize/', blank=True)
    variants_type_choises = (('Тест один правильный ответ', 'Тест один правильный ответ'),
                             ('Тест несколько правильных ответов', 'Тест несколько правильных ответов'),
                             ('Тест на последовательность', 'Тест на последовательность'),
                             ('Тест на соответствие', 'Тест на соответствие'))
    variants_type = models.CharField(verbose_name='Тип вопроса', max_length=55, blank=False, choices=variants_type_choises)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-pk']

    def __str__(self):
        return self.question_text

    def get_teacher_first_column_answers(self):
        return Answer.objects.filter(question_id=self).order_by('first_columnn').exclude(first_columnn=0)

    def get_teacher_second_column_answers(self):
        return Answer.objects.filter(question_id=self).order_by('second_column').exclude(second_column=0)

class Answer(models.Model):
    question_id = models.ForeignKey(Question, verbose_name='Bопрос', related_name='answer_question_id', on_delete=models.CASCADE)
    ansr_text = RichTextUploadingField(verbose_name='Текст ответа:', max_length=345, blank=False)
    answer_right = models.BooleanField(verbose_name='Ответ верен?', default=False)
    first_columnn = models.IntegerField(verbose_name='Первый столбец(позиция)', default=0)
    second_column = models.IntegerField(verbose_name='Второй столбец(позиция)', default=0)

    class Meta:
        verbose_name = 'Текст ответа'
        verbose_name_plural = 'Текст ответа'

    def clean(self):
        errors = {}
        if self.question_id.variants_type == 'Тест один правильный ответ':
            if Answer.objects.get(pk=self.pk).answer_right == False and self.answer_right == True:
                if Answer.objects.filter(question_id=self.question_id, answer_right=True).count() + 1 > 1:
                    errors['answer_right'] = 'В тесте доступен только 1 правильный ответ'
        if errors:
            raise ValidationError(errors)



