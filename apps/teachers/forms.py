from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django_select2.forms import ModelSelect2Widget

from apps.educational_materials.models import *
from core.models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'date_joined',
                   'user_permissions', 'groups', 'deaprtment_id', 'all_department_id',]

class PswChangeForm(SetPasswordForm):
    class Meta:
        model = Teacher
        exclude = []

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        exclude = ('department_id', )

class DisciplineAccessForm(forms.ModelForm):
    group_id = forms.ModelChoiceField(
        queryset=StudentGroupQuide.objects.none(),

        label=('Группa'),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = DisciplineAccess
        exclude = ('parent_id', )

    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        aviable_groups = list(DisciplineAccess.objects.filter(parent_id=instance.parent_id)
                              .exclude(group_id=instance.group_id))
        super(DisciplineAccessForm, self).__init__(*args, **kwargs)
        self.fields['group_id'].queryset = StudentGroupQuide.objects.all().exclude(name__in=aviable_groups)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('discipline_id', )

class TopicAccessForm(forms.ModelForm):
    group_id = forms.ModelChoiceField(
        queryset=StudentGroupQuide.objects.none(),

        label=('Группa'),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta(forms.ModelForm):
        model = TopicAccess
        exclude = ('parent_id', )

    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        aviable_groups = list(DisciplineAccess.objects.filter(parent_id=instance.parent_id.discipline_id))
        disabled_groups = list(TopicAccess.objects.filter(parent_id=instance.parent_id).exclude(group_id=instance.group_id))
        super(TopicAccessForm, self).__init__(*args, **kwargs)
        self.fields['group_id'].queryset = StudentGroupQuide.objects.all().filter(name__in=aviable_groups)\
            .exclude(name__in=disabled_groups)

class QuestionsCopyForm(forms.Form):
    title = forms.ModelChoiceField(
        queryset=Topic.objects.none(),

        label=('Тема'),
            widget=ModelSelect2Widget(
                search_fields=["title__icontains"],
                max_results=500,
                attrs={'style': 'width: 100%'},
            ),
    )

    def __init__(self,  **kwargs):
        super(QuestionsCopyForm, self).__init__()
        self.fields['title'].queryset = Topic.objects.all().exclude(pk__in=kwargs['topics_to_exclude'])

class AnswerForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(), label='Текст ответа', required=True)

