from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import LoginForm, StudentCreateForm
from core.models import SystemQuide


# Create your views here.
class LoginPage(LoginView):
    template_name = 'core/account/login.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginPage, self).get_context_data(**kwargs)
        context['registration'] = SystemQuide.objects.get(pk=1).front_registration
        return context

    def get_success_url(self):
        self.success_url = 'main'
        if self.request.user.groups.get().name == 'teachers':
            self.success_url = 'teacher_urls:personal_account_url'
        elif self.request.user.groups.get().name == 'students':
            self.success_url = 'students_urls:st_personal_account_url'
        else:
            self.success_url = 'main'
        return reverse_lazy(self.success_url)

class StudentRegisterPage(CreateView):
    template_name = 'core/account/registration_student.html'
    form_class = StudentCreateForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated or SystemQuide.objects.get(pk=1).front_registration == False:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Успешная регистрация!')
        return reverse_lazy('core_urls:registration_student_url')
