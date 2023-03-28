from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.views.generic import TemplateView, UpdateView, DetailView

from apps.educational_materials.models import DisciplineAccess, TopicAccess
from django.utils import timezone

from apps.students.forms import *
from core.decorators import students_check
from core.models import Student, StudentGroupQuide

students_decorators = [login_required, user_passes_test(students_check), ]

# Create your views here.
class PersonalAccount(object):
    template_name = 'student/student_office/personal_account.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalAccount, self).get_context_data(**kwargs,)
        group_id = get_object_or_404(Student, username=self.request.user.username).active_group_id
        context['discipline_aviable'] = DisciplineAccess.objects.filter(group_id=group_id,
                                                                        discipline_access_end__gte=timezone.now(),
                                                                        discipline_access_start__lte=timezone.now(),
                                                                        parent_id__status=True)
        context['discipline_unaviable'] = DisciplineAccess.objects.filter(group_id=group_id,
                                                                          discipline_access_end__lte=timezone.now(),
                                                                          parent_id__status=True)
        return context

@method_decorator(students_decorators, name='dispatch')
class StudentPersonalAccount(PersonalAccount, TemplateView,):
    tab = 'tab1'

    def get_context_data(self, **kwargs):
        context = super(StudentPersonalAccount, self).get_context_data(**kwargs,)
        context['user'] = get_object_or_404(Student, username=self.request.user.username)
        return context

    def post(self, request, *args, **kwargs):
        student = self.get_context_data().get('user')
        if self.request.POST.get('_pk').isdigit():
            if StudentGroupQuide.objects.filter(pk=self.request.POST.get('_pk')).exists():
                group = StudentGroupQuide.objects.get(pk=self.request.POST.get('_pk'))
                if group in student.all_group_id.all():
                    student.active_group_id = group
                    student.save()

        return redirect('students_urls:st_personal_account_url')

@method_decorator(students_decorators, name='dispatch')
class StudentPersonalChange(PersonalAccount, UpdateView):
    tab = 'tab4'
    form_class = StudentForm
    success_url = reverse_lazy('students_urls:st_personal_account_change_url')

    def get_object(self, queryset=None):
        return get_object_or_404(Student, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(StudentPersonalChange, self).get_context_data(**kwargs, )
        context['change_password_from'] = PswChangeForm(user=self.object)
        return context

    def form_valid(self, form):
        messages.success(self.request, ('Данные изменены!'))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if '_change_password' in request.POST:
            password_form = PswChangeForm(self.get_object(), self.request.POST,)
            if password_form.is_valid():
                messages.success(self.request, ('User Passsword was updated successfully!'))
                password_form.save()
            else:
                messages.error(self.request, (password_form.error_messages.get('password_mismatch')))
            return redirect('teacher_urls:personal_account_change_url')

        return super().post(request, *args, **kwargs)

@method_decorator(students_decorators, name='dispatch')
class StudentDiscipines(PersonalAccount, TemplateView):
    tab = ''

    def get_context_data(self, **kwargs):
        context = super(StudentDiscipines, self).get_context_data(**kwargs, )
        if self.tab == 'tab2':
            context['instances'] = context.get('discipline_aviable')
        elif self.tab == 'tab3':
            context['instances'] = context.get('discipline_unaviable')
        return context

@method_decorator(students_decorators, name='dispatch')
class DiscipineDetail(DetailView):
    template_name = 'student/student_office/instance_detail.html'
    context_object_name = 'instance'

    def get_queryset(self):
        group_id = get_object_or_404(Student, username=self.request.user.username).active_group_id
        quesryset = DisciplineAccess.objects.filter(group_id=group_id, parent_id__status=True,
                                                    discipline_access_start__lte=timezone.now())

        return quesryset

@method_decorator(students_decorators, name='dispatch')
class TopicDetail(DiscipineDetail):

    def get_queryset(self):

        group_id = get_object_or_404(Student, username=self.request.user.username).active_group_id
        quesryset = TopicAccess.objects.filter(group_id=group_id, parent_id__status=True,
                                               parent_id__discipline_id__status=True,
                                               discipline_access_start__lte=timezone.now())

        return quesryset

