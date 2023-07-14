from django.db import models

from apps.educational_materials.models import DisciplineAccess, TopicAccess, Question
from apps.journals.models import QuizeLogDeciplineJournal, QuizeLogTopicJournal
from core.models import Student



class QuizeRezultObject(models.Model):
    user = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE,
                             related_name="%(app_label)s_%(class)s_related",)
    current_question = models.ForeignKey(Question, verbose_name='Tекущий вопрос', on_delete=models.CASCADE, null=True,)
    final_quize = models.BooleanField('Итоговый тест?', default=False)
    ended_quize = models.BooleanField('Тест сдавался?', default=False)
    quize_started_it = models.DateTimeField('Дата начала сдачи теста(seconds)', null=True, )

    class Meta:
        abstract = True

    def get_user_questions(self):
        if self._meta.model_name == 'quizerezultdecepline':
            quize_rezults = QuizeLogDeciplineJournal
        elif self._meta.model_name == 'quizerezulttopic':
            quize_rezults = QuizeLogTopicJournal
        return quize_rezults.objects.filter(parent_id=self.parent_id.pk, user_id=self.user.pk)


    def get_correct_answers(self):
        return self.get_user_questions().filter(answer_right=True).count()


    def get_correct_answers_percent(self):
        if self.parent_id.quiestion_quantity != 0:
            return round((self.get_correct_answers() / self.parent_id.quiestion_quantity) * 100)
        else:
            return 0

    def get_estimation(self):
        estimation = 0
        correct_answers_percent = self.get_correct_answers_percent()
        if correct_answers_percent >= 71 and correct_answers_percent <= 80:
            estimation = 3
        elif correct_answers_percent >= 81 and correct_answers_percent <= 90:
            estimation = 4
        elif correct_answers_percent >= 91 and correct_answers_percent <= 100:
            estimation = 5

        return estimation

class QuizeRezultDecepline(QuizeRezultObject):
    parent_id = models.ForeignKey(DisciplineAccess, verbose_name='Дисциплинa:', on_delete=models.CASCADE,
                                  related_name='quize_declpline_rezult_discipline_id', )

    class Meta:
        verbose_name = 'Дисциплинa(Результат теста)'
        verbose_name_plural = 'Дисциплины(Результат тестов)'
        unique_together = ['parent_id', 'user', ]


class QuizeRezultTopic(QuizeRezultObject):
    parent_id = models.ForeignKey(TopicAccess, verbose_name='Тема:', on_delete=models.CASCADE,
                                  related_name='quize_topic_rezult_topic_id', )

    class Meta:
        verbose_name = 'Тема(Результат теста)'
        verbose_name_plural = 'Темы(Результат тестов)'
        unique_together = ['parent_id', 'user', ]

