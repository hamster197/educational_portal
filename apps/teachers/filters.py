import django_filters

from apps.educational_materials.models import Question


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = {
            'question_text': ['icontains'],
        }
