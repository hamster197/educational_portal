from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget
from hcaptcha.fields import hCaptchaField

from core.models import Student, StudentGroupQuide


class LoginForm(AuthenticationForm):
    hcaptcha = hCaptchaField(theme='dark', size='compact', )
    class Meta:
        model = User
        exclude = []

class StudentCreateForm(UserCreationForm):
    hcaptcha = hCaptchaField(theme='dark', size='compact')
    active_group_id = forms.ModelChoiceField(
        queryset=StudentGroupQuide.objects.all(),
        label=('Группa'),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = Student
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'date_joined',
                   'user_permissions', 'groups', 'all_group_id', ]