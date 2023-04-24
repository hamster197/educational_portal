from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.views.generic import TemplateView, UpdateView, DetailView

from apps.educational_materials.models import DisciplineAccess, TopicAccess, Answer
from django.utils import timezone

from apps.journals.models import QuizeLogTopicJournal, QuizeLogDeciplineJournal
from apps.students.core import check_for_aviable_quize_rezult, get_for_aviable_quize_access, \
    get_or_create_for_aviable_quize_rezult, get_timer, get_aviable_questions
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

class QuizeObject(DetailView):
    context_object_name = 'instance'
    now = timezone.now()
    quize_status = False

    def setup(self, request, *args, **kwargs):
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if get_for_aviable_quize_access(self, ).filter(final_quize_start__lte=self.now, \
                                                       final_quize_end__gte=self.now).exists():
            self.quize_status = True

    def get_context_data(self, **kwargs):
        context = super(QuizeObject, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.request.user.pk)

        return context

@method_decorator(students_decorators, name='dispatch')
class QuizeApproval(QuizeObject):
    template_name = 'student/quize/quize_approval.html'

    def get_queryset(self):
        if self.model == DisciplineAccess:
            return get_for_aviable_quize_access(self, ).filter(parent_id__status=True)
        elif self.model == TopicAccess:
            return get_for_aviable_quize_access(self, ).filter(parent_id__status=True,
                                                                       parent_id__discipline_id__status=True,)

    def post(self, request, *args, **kwargs):

        get_or_create_for_aviable_quize_rezult(self)
        if self.model == DisciplineAccess:
            return redirect('students_urls:decepline_quize_test_url', pk=self.get_object().pk)
        elif self.model == TopicAccess:
            return redirect('students_urls:topic_quize_test_url', pk=self.get_object().pk)



@method_decorator(students_decorators, name='dispatch')
class QuizeRezult(QuizeObject):
    template_name = 'student/quize/quize_rezult.html'

    def get_queryset(self):

        if self.model == DisciplineAccess:
            queryset = get_for_aviable_quize_access(self, ).filter(
                quize_declpline_rezult_discipline_id__user=self.request.user,)
        elif self.model == TopicAccess:
            queryset = get_for_aviable_quize_access(self, ).filter(
                quize_topic_rezult_topic_id__user=self.request.user,)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuizeRezult, self).get_context_data(**kwargs)
        if get_timer(self) <= 0:
            context['timeout'] = 'TimeOut'
        context['estimation'] = check_for_aviable_quize_rezult(self,)

        return context

@method_decorator(students_decorators, name='dispatch')
class QuizeTest(QuizeObject):
    template_name = 'student/quize/quize_test_main.html'

    def dispatch(self, request, *args, **kwargs):
        if check_for_aviable_quize_rezult(self) is not None:
            return redirect(self.model.get_rezult_url(self),)
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)

    def get_queryset(self):
        return get_for_aviable_quize_access(self,)

    def get_context_data(self, **kwargs):
        get_aviable_questions(self)
        context = super(QuizeObject, self).get_context_data(**kwargs)
        quize_rezult = get_or_create_for_aviable_quize_rezult(self)
        context['quize_rezult'] = quize_rezult
        if quize_rezult.current_question.variants_type == 'Тест один правильный ответ' \
                or quize_rezult.current_question.variants_type == 'Тест несколько правильных ответов':
            context['answers'] = quize_rezult.current_question.answer_question_id.all().order_by('?')
        elif quize_rezult.current_question.variants_type == 'Тест на последовательность':
            context['answers'] = quize_rezult.current_question.get_teacher_first_column_answers().order_by('?')
        elif quize_rezult.current_question.variants_type == 'Тест на соответствие':
            context['answers_1'] = quize_rezult.current_question.get_teacher_first_column_answers()
            context['answers_2'] = quize_rezult.current_question.get_teacher_second_column_answers().order_by('?')
        context['timer'] = get_timer(self)

        return context

    def post(self, request, *args, **kwargs):

        if get_timer(self) <= 0 or not get_aviable_questions(self):
            return redirect(self.model.get_absolute_url(self), )

        answers_right = False
        self.object = self.get_object()
        quize_rezult = self.get_context_data().get('quize_rezult')

        if '_answers' in self.request.POST:
            if quize_rezult.current_question.variants_type == 'Тест один правильный ответ' \
                or quize_rezult.current_question.variants_type == 'Тест несколько правильных ответов':
                request_answers = Answer.objects.filter(pk__in=self.request.POST.getlist('_answers'), answer_right=True,
                                                        question_id=quize_rezult.current_question)
                if request_answers.count() != 0:
                    if quize_rezult.current_question.variants_type == 'Тест один правильный ответ' \
                            and len(self.request.POST.getlist('_answers')) == 1:
                        answers_right = True
                    if quize_rezult.current_question.variants_type == 'Тест несколько правильных ответов':
                        question_answers = Answer.objects.filter(answer_right=True,
                                                                question_id=quize_rezult.current_question)
                        if question_answers.count() == request_answers.count():
                            answers_right = True

            elif quize_rezult.current_question.variants_type == 'Тест на последовательность' \
                    or quize_rezult.current_question.variants_type == 'Тест на соответствие':
                request_answer = self.request.POST.getlist('_answers')
                if quize_rezult.current_question.variants_type == 'Тест на последовательность':
                    correct_answers = quize_rezult.current_question.get_teacher_first_column_answers()\
                        .values_list('pk', flat=True)
                if quize_rezult.current_question.variants_type == 'Тест на соответствие':
                    correct_answers = quize_rezult.current_question.get_teacher_second_column_answers()\
                        .values_list('pk', flat=True)
                request_answer = [int(x) for x in request_answer]
                if request_answer == list(correct_answers):
                    answers_right = True

        if self.model == DisciplineAccess:
            journal_log_instance = QuizeLogDeciplineJournal
        elif self.model == TopicAccess:
            journal_log_instance = QuizeLogTopicJournal
        user = self.request.user
        journal_log_instance.objects.create(parent_id=self.object.pk, parent_name=quize_rezult.parent_id,
                                            question_id=quize_rezult.current_question.pk, user_id=user.pk,
                                            user_full_name=user.first_name + ' ' + user.last_name + ' (' +
                                                           user.username + ')', answer_right=answers_right,
                                            test_type=quize_rezult.final_quize)

        if quize_rezult.get_user_questions().count() == self.object.quiestion_quantity:
            quize_rezult.ended_quize = True
        quize_rezult.save()

        return redirect(self.model.get_testing_url(self),)





