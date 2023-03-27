from django import forms
from django.contrib.auth.forms import SetPasswordForm

from core.models import Student, Teacher


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'date_joined',
                   'user_permissions', 'groups', 'active_group_id', 'all_group_id',]

class PswChangeForm(SetPasswordForm):
    class Meta:
        model = Student
        exclude = []