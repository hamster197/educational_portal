from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.

class FacultyQuide(models.Model):
    name = models.CharField(verbose_name='Название', max_length=355, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник факультетов'
        verbose_name_plural = 'Справочник факультетов'

class DepartmentQuide(models.Model):
    name = models.CharField('Название', max_length=355, blank=False, unique=True)
    faculty_id = models.ForeignKey(FacultyQuide, verbose_name='Факультет', related_name='department_faculty_id',
                                 on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник кафедр'
        verbose_name_plural = 'Справочник кафедр'

class StudentGroupQuide(models.Model):
    faculty_id = models.ForeignKey(FacultyQuide, related_name="group_faculty_id", on_delete=models.CASCADE,
                             verbose_name='Факультет', null=False)
    name = models.CharField('Группы(студенты):', max_length=55,
                            blank=False, null=False, unique=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник групп'
        verbose_name_plural = 'Справочник групп'

class SystemQuide(models.Model):
    feed_group_id = models.ForeignKey(StudentGroupQuide, verbose_name='Группы для импорта из фида(админка)',
                                                         related_name='system_quide_feed_group_id',
                                                         on_delete=models.CASCADE, null=False)
    front_registration = models.BooleanField(verbose_name='Регистрация с фронта?', default=False)

    class Meta:
        verbose_name = 'Системный справочник(Настройки)'
        verbose_name_plural = 'Системный справочник(Настройки)'

class MainUser(AbstractUser):
    first_name = models.CharField('Имя', max_length=45, blank=False,)
    last_name = models.CharField('Фамилия', max_length=45, blank=False, )
    email = models.EmailField('Email', unique=True, null=True)
    patronymic = models.CharField('Oтчество', max_length=45, blank=True)
    
    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'

class Student(MainUser):
    grade_book_number = models.CharField('Номер зачетной книжки', max_length=25, default='n/a')
    active_group_id = models.ForeignKey(StudentGroupQuide, related_name='student_active_group_id',
                                         on_delete=models.CASCADE, verbose_name='Группа(Активная):')
    all_group_id = models.ManyToManyField(StudentGroupQuide, related_name='student_all_group_id',
                                   verbose_name='Все доступные группы:', blank=True, )

    def __str__(self):
        full_name = self.last_name + ' ' + self.first_name
        if self.patronymic:
            full_name = full_name + ' ' + self.patronymic
        return full_name

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Все студенты'

    # def get_decepline_queryset(self, access):
    #     from apps.students.models import QuizeRezultDecepline
    #     return QuizeRezultDecepline.objects.filter(parent_id=access, user_id=self.pk)
    #
    # def get_topic_queryset(self, access):
    #     from apps.students.models import QuizeRezultTopic
    #     return QuizeRezultTopic.objects.filter(parent_id=access, user_id=self.pk)
    #
    # def get_quize_estimation(self, access, type):
    #     estimation = 'N/A'
    #     from apps.educational_materials.models import DisciplineAccess, TopicAccess
    #     if type == DisciplineAccess:
    #         rezult = self.get_decepline_queryset(access)
    #     elif type == TopicAccess:
    #         rezult = self.get_topic_queryset(access)
    #     if rezult.exists():
    #         estimation = str(rezult.first().get_estimation()) + ' ' + str(rezult.first().get_correct_answers_percent())\
    #                         + '% ' +str(rezult.first().get_correct_answers()) + ' Correct Answers'
    #     return estimation


class Teacher(MainUser):
    deaprtment_id = models.ForeignKey(DepartmentQuide, related_name='teacher_deaprtment_id', on_delete=models.CASCADE,
                                   verbose_name='Кафедра(Активная):', )
    all_department_id = models.ManyToManyField(DepartmentQuide, related_name='teacher_all_department_id',
                                   verbose_name='Все доступные кафедры:', blank=True, )

    def __str__(self):
        full_name = self.last_name + ' ' + self.first_name
        if self.patronymic:
            full_name = full_name + ' ' + self.patronymic
        return full_name

    class Meta:
        verbose_name = 'Преподаватели'
        verbose_name_plural = 'Все преподаватели'

