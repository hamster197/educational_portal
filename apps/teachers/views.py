from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, CreateView, RedirectView, FormView, DetailView
from django_filters.views import FilterView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from apps.students.models import QuizeRezultTopic, QuizeRezultDecepline
from apps.teachers.core import questions_copy_core, get_report_card_queryset, get_final_quize_status
from apps.teachers.filters import QuestionFilter
from apps.teachers.forms import *
from core.decorators import teachers_check, teacher_displine_access
from core.models import Teacher, DepartmentQuide

teachers_decorators = [login_required, user_passes_test(teachers_check), ]
teachers_decorators_descepline = [login_required, teacher_displine_access, user_passes_test(teachers_check), ]

# Create your views here.
class PersonalAccount(object):
    template_name = 'teacher/teacher_office/personal_account.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalAccount, self).get_context_data(**kwargs,)
        department_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        context['discipline_published'] = Discipline.objects.filter(department_id=department_id,
                                                                        status=True)
        context['discipline_unpublished'] = Discipline.objects.filter(department_id=department_id,
                                                                          status=False)
        return context

@method_decorator(teachers_decorators, name='dispatch')
class TeacherPersonalAccount(PersonalAccount, TemplateView):
    tab = 'tab1'

    def get_context_data(self, **kwargs):
        context = super(TeacherPersonalAccount, self).get_context_data(**kwargs,)
        context['user'] = get_object_or_404(Teacher, username=self.request.user.username)
        return context

    def post(self, request, *args, **kwargs):
        teacher = self.get_context_data().get('user')
        if self.request.POST.get('_pk').isdigit():
            if DepartmentQuide.objects.filter(pk=self.request.POST.get('_pk')).exists():
                department = DepartmentQuide.objects.get(pk=self.request.POST.get('_pk'))
                if department in teacher.all_department_id.all():
                    teacher.deaprtment_id = department
                    teacher.save()

        return redirect('teacher_urls:personal_account_url')

@method_decorator(teachers_decorators, name='dispatch')
class TeacherPersonalChange(PersonalAccount, UpdateView):
    tab = 'tab4'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_urls:personal_account_change_url')

    def get_object(self, queryset=None):
        return get_object_or_404(Teacher, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(TeacherPersonalChange, self).get_context_data(**kwargs, )
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

@method_decorator(teachers_decorators, name='dispatch')
class TeacherDiscipine(PersonalAccount, TemplateView):
    tab = ''

    def get_context_data(self, **kwargs):
        context = super(TeacherDiscipine, self).get_context_data(**kwargs, )
        if self.tab == 'tab2':
            context['disciplines'] = context.get('discipline_unpublished')
        elif self.tab == 'tab3':
            context['disciplines'] = context.get('discipline_published')
        return context


@method_decorator(teachers_decorators, name='dispatch')
class DiscipineCreate(CreateView):
    form_class = DisciplineForm
    template_name = 'teacher/educational_materials/material_edit.html'

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:discipline_edit_url', kwargs={'discipine_pk': self.object.pk })

@method_decorator(teachers_decorators_descepline, name='dispatch')
class DiscipineEdit(UpdateView):
    form_class = DisciplineForm
    template_name = 'teacher/educational_materials/material_edit.html'
    type = 'discipline'
    pk_url_kwarg = 'discipine_pk'
    model = Discipline

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:discipline_edit_url', kwargs={'discipine_pk': self.kwargs['discipine_pk']})

@method_decorator(teachers_decorators_descepline, name='dispatch')
class DisciplineAccessCreate(RedirectView, ):

    def dispatch(self, request, *args, **kwargs):
        if get_object_or_404(Teacher, pk=self.request.user.pk).deaprtment_id != \
                get_object_or_404(Discipline,pk=self.kwargs['discipine_pk']).department_id:
            return redirect('teacher_urls:personal_account_url')

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):

        disciline = get_object_or_404(Discipline, pk=self.kwargs['discipine_pk'])
        new_discipline_access = DisciplineAccess.objects.create(parent_id=disciline)
        url = reverse_lazy('teacher_urls:discipline_access_edit_url',
                           kwargs={'discipine_pk': self.kwargs['discipine_pk'], 'pk': new_discipline_access .pk})
        return url

@method_decorator(teachers_decorators_descepline, name='dispatch')
class DisciplineAccessEdit(UpdateView):
    form_class = DisciplineAccessForm
    template_name = 'teacher/educational_materials/access_edit.html'
    type = 'Дисциплина'
    model = DisciplineAccess

    def get_queryset(self):
        deaprtment_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        return DisciplineAccess.objects.filter(parent_id__department_id=deaprtment_id)

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:discipline_access_edit_url', kwargs={'discipine_pk': self.object.parent_id.pk,
                                                                               'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, ('Данные не сохранены!'))
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(teachers_decorators_descepline, name='dispatch')
class TopicCreate(CreateView,):
    form_class = TopicForm
    template_name = 'teacher/educational_materials/material_edit.html'
    type = 'topic_create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.discipline_id = get_object_or_404(Discipline, pk=self.kwargs['discipine_pk'])
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:discipline_edit_url', kwargs={'discipine_pk': self.kwargs['discipine_pk']})

@method_decorator(teachers_decorators, name='dispatch')
class TopicEdit(UpdateView):
    form_class = TopicForm
    template_name = 'teacher/educational_materials/material_edit.html'
    type = 'Тема'

    def get_queryset(self):
        deaprtment_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        return Topic.objects.filter(discipline_id__department_id=deaprtment_id)

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:discipline_edit_url', kwargs={'discipine_pk': self.object.discipline_id.pk })


@method_decorator(teachers_decorators_descepline, name='dispatch')
class TopicAccessCreate(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        topic = Topic.objects.get(pk=self.kwargs['theme_pk'])
        topic_access_counter = topic.topic_access_parent_id.all().count()
        disciplines_access_counter = topic.discipline_id.discipline_access_parent_id.all().count()
        status = True
        if topic.discipline_id.department_id != get_object_or_404(Teacher, pk=self.request.user.pk).deaprtment_id:
            status = False
        if disciplines_access_counter != 0:
            if disciplines_access_counter <= topic_access_counter:
                messages.success(self.request, ('Добавьте доступ группы к дисциплине!'))
                status = False
        if status == False:
            return redirect('teacher_urls:topic_edit_url', pk=self.kwargs['theme_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):

        theme = get_object_or_404(Topic, pk=self.kwargs['theme_pk'])
        new_topic_access = TopicAccess.objects.create(parent_id=theme)
        url = reverse_lazy('teacher_urls:topic_access_edit_url',
                           kwargs={'discipine_pk': self.kwargs['discipine_pk'], 'pk': new_topic_access.pk})
        return url

@method_decorator(teachers_decorators_descepline, name='dispatch')
class TopicAccessEdit(UpdateView):
    form_class = TopicAccessForm
    template_name = 'teacher/educational_materials/access_edit.html'
    type = 'Тема'

    def get_queryset(self):
        deaprtment_id = get_object_or_404(Teacher, username=self.request.user.username).deaprtment_id
        return TopicAccess.objects.filter(parent_id__discipline_id__department_id=deaprtment_id)

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:topic_access_edit_url', kwargs={'discipine_pk': self.object.parent_id.discipline_id.pk,
                                                                               'pk': self.object.pk})
    def form_invalid(self, form):
        messages.error(self.request, ('Данные не сохранены!'))
        return self.render_to_response(self.get_context_data(form=form))

@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionsList(FilterView, FormView):
    template_name = 'teacher/educational_materials/questions_list.html'
    context_object_name = 'instances'
    filterset_class = QuestionFilter
    form_class = QuestionsCopyForm
    paginate_by = 10
    topic = None

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'], discipline_id__pk=self.kwargs['discipine_pk'])
        return Question.objects.filter(topic_access=self.topic)

    def get_form_kwargs(self):
        self.object_list = self.get_queryset()
        kwargs = super().get_form_kwargs()
        if self.object_list.first():
            kwargs['topics_to_exclude'] = list(self.object_list.first().topic_access.all().values_list('id', flat=True))
        else:
            kwargs['topics_to_exclude'] = []
        return kwargs

    def post(self, request, *args, **kwargs):
        if 'title' in self.request.POST:
            author = self.request.user
            topic = get_object_or_404(Topic, pk=self.request.POST.get('title'))
            messages.success(self.request, ('В тему ' + topic.title + ' перенесенено ' \
                                            + str(questions_copy_core(Topic.objects.get(pk=self.kwargs['topic_pk']), topic, author)) \
                                            + ' воросов'))
            return self.form_valid(self.get_form())
        else:
            messages.success(self.request, ('Данные не сохранены!'))
            return self.form_invalid(self.get_form())

    def get_success_url(self):
        return reverse_lazy('teacher_urls:question_list_url', kwargs={'topic_pk': self.kwargs['topic_pk'],
                                                                      'discipine_pk':self.kwargs['discipine_pk'], })


class AnswerInline(InlineFormSetFactory):
    model = Answer
    fields = ['ansr_text', 'answer_right']
    factory_kwargs = {'extra': 2, 'max_num': None,
                      'can_delete': True}

class QuestionEditMixin(object):
    model = Question
    inlines = [AnswerInline,]
    fields = ['question_text', 'image']
    template_name = 'teacher/educational_materials/question_simple_edit.html'
    topic = ''

    def get_success_url(self):
        messages.success(self.request, ('Данные сохранены!'))
        return reverse_lazy('teacher_urls:question_edit_url', kwargs={'pk': self.object.pk,
                                                                      'topic_pk': self.kwargs['topic_pk'],
                                                                      'discipine_pk':self.kwargs['discipine_pk'],
                                                                      })


    def forms_invalid(self, form, inlines):
        messages.success(self.request, ('Данные не сохранены!'))
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form, inlines=inlines))

@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionEdit(QuestionEditMixin, UpdateWithInlinesView, ):

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'], discipline_id__pk=self.kwargs['discipine_pk'])
        variants = ['Тест один правильный ответ', 'Тест несколько правильных ответов']
        return Question.objects.filter(topic_access=self.topic, variants_type__in=variants)



@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionCreate(QuestionEditMixin, CreateWithInlinesView,):
    action = ''

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs, )
        if self.action == 'one':
            context['type'] = 'Тест один правильный ответ'
        elif self.action == 'not_one':
            context['type'] = 'Тест несколько правильных ответов'
        context['topic'] = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])

        return context

    def forms_valid(self, form, inlines, **kwargs):
        self.object = form.save(commit=False)
        if self.action == 'one':
            type = 'Тест один правильный ответ'
        elif self.action == 'not_one':
            type = 'Тест несколько правильных ответов'
        self.object.variants_type = type
        form.save()

        self.object.topic_access.add(self.get_context_data(form=form, **kwargs)['topic'])
        for formset in inlines:
            formset.save()

        return super().forms_valid(form, inlines,)

@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionSequenceEdit(UpdateView ):
    template_name = 'teacher/educational_materials/question_sequence_edit.html'
    model = Question
    fields = ['question_text', 'image']
    topic = ''

    def get_context_data(self, **kwargs):
        context = super(QuestionSequenceEdit, self).get_context_data(**kwargs, )
        context['answer_form'] = AnswerForm()
        context['type_of_edit'] = 'Редактирование вопроса'
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'], discipline_id__pk=self.kwargs['discipine_pk'])
        return Question.objects.filter(topic_access=self.topic, variants_type='Тест на последовательность')


    def form_valid(self, form):
        self.object = form.save()

        if self.request.POST.get('text'):
            Answer.objects.create(question_id=self.object, ansr_text=self.request.POST.get('text'),
                                  first_columnn=Answer.objects.filter(question_id=self.object).count() + 1)



        request_data = list(self.request.POST)
        unnecessary_values = ['csrfmiddlewaretoken', 'question_text', 'image', 'text', ]
        for value in unnecessary_values:
            request_data.remove(value)

        if '_variant_question_answer_delete' in request_data:
            request_data.remove('_variant_question_answer_delete')
            Answer.objects.filter(pk=self.request.POST.get('_variant_question_answer_delete',)).delete()

        saved_answers = Answer.objects.filter(question_id=self.object).count()
        if self.request.POST.get('text'):
            saved_answers -= 1
        if saved_answers != Answer.objects.filter(pk__in=request_data).count():
            messages.error(self.request, ('Не все данные сохранены!'))
            return super().form_invalid(form)

        counter = 0
        for data in request_data:
            counter += 1
            Answer.objects.filter(pk=data).update(first_columnn=counter,)

        messages.success(self.request, ('Данные сохранены!'))

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, ('Данные не сохранены!'))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('teacher_urls:question_edit_sequence_url', kwargs={'discipine_pk': self.topic.discipline_id.pk,
                                                                               'topic_pk': self.topic.pk, 'pk': self.object.pk})

@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionSequenceComplianceCreate(CreateView, ):
    template_name = 'teacher/educational_materials/question_sequence_edit.html'
    model = Question
    fields = ['question_text', 'image']
    question_type = ''

    def get_context_data(self, **kwargs):
        context = super(QuestionSequenceComplianceCreate, self).get_context_data(**kwargs, )
        context['topic'] = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        context['type_of_question'] = self.question_type
        context['type_of_edit'] = 'Новый вопрос'
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.variants_type = self.question_type
        self.object.save()
        self.object.topic_access.add(self.get_context_data().get('topic'))
        messages.success(self.request, ('Данные сохранены!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, ('Данные не сохранены!'))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        topic = self.get_context_data().get('topic')
        if self.question_type == 'Тест на последовательность':
            url = 'teacher_urls:question_edit_sequence_url'
        elif self.question_type == 'Тест на соответствие':
            url = 'teacher_urls:question_edit_compliance_url'

        return reverse_lazy(url, kwargs={'discipine_pk': topic.discipline_id.pk, 'topic_pk': topic.pk,'pk': self.object.pk})

@method_decorator(teachers_decorators_descepline, name='dispatch')
class QuestionComplianceEdit(UpdateView):
    template_name = 'teacher/educational_materials/question_compliance_edit.html'
    model = Question
    fields = ['question_text', 'image']
    topic = ''

    def get_context_data(self, **kwargs):
        context = super(QuestionComplianceEdit, self).get_context_data(**kwargs, )
        context['answer_form'] = AnswerForm()
        context['type_of_edit'] = 'Редактирование вопроса'
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'], discipline_id__pk=self.kwargs['discipine_pk'])
        return Question.objects.filter(topic_access=self.topic, variants_type='Тест на соответствие')


    def form_valid(self, form):

        self.object = form.save()
        request_data = list(self.request.POST)

        if '_variant_question_answer_delete' in self.request.POST:
            positon = self.request.POST.get('_variant_question_answer_delete')
            from django.db.models import Q
            Answer.objects.filter(Q(first_columnn=positon) | Q(second_column=positon), question_id=self.object,).delete()
            request_data.remove('_variant_question_answer_delete')

        all_answers =Answer.objects.filter(question_id=self.object).count()

        new_answers = []
        if '_add_answer' in self.request.POST:
            new_answers.append(Answer(question_id=self.object, first_columnn=(all_answers / 2) + 1))
            new_answers.append(Answer(question_id=self.object, second_column=(all_answers / 2) + 1))
            request_data.remove('_add_answer')

        unnecessary_values = ['csrfmiddlewaretoken', 'question_text', 'image',]
        for value in unnecessary_values:
            request_data.remove(value)

        if all_answers != Answer.objects.filter(pk__in=request_data, question_id=self.object).count():
            messages.error(self.request, ('Данные не сохранены!'))
            return super().form_invalid(form)

        counter = 0
        all_answers = int(Answer.objects.filter(question_id=self.object).count()/2)
        for data in request_data:
            counter = counter + 1
            if counter <= all_answers:
                Answer.objects.filter(pk=data).update(first_columnn=counter, ansr_text=self.request.POST.get(data),
                                                      second_column=0,)
            else:
                new_counter = counter - all_answers
                Answer.objects.filter(pk=data).update(second_column=new_counter, ansr_text=self.request.POST.get(data),
                                                      first_columnn=0,)

        Answer.objects.bulk_create(new_answers)
        messages.success(self.request, ('Данные сохранены!'))

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, ('Данные не сохранены!'))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('teacher_urls:question_edit_compliance_url', kwargs={'discipine_pk': self.topic.discipline_id.pk,
                                                                               'topic_pk': self.topic.pk,'pk': self.object.pk})


@method_decorator(user_passes_test(teachers_check), name='dispatch')
class ReportCard(DetailView):
    template_name = 'teacher/teacher_office/report_card.html'
    context_object_name = 'access'
    quize_type = ''
    action = 'List'
    def get_queryset(self):
        return get_report_card_queryset(self)

    def get_context_data(self, **kwargs):
        context = super(ReportCard, self).get_context_data(**kwargs,)
        from django.db.models import Subquery, OuterRef
        context['final_quize_status'] = get_final_quize_status(self)
        context['all_users_rezults'] = self.quize_type.objects.filter(parent_id=self.object, ended_quize=True,
                                                                      final_quize=context['final_quize_status'])
        all_users_rezults_subquery = context['all_users_rezults'].filter(user=OuterRef("pk"),)

        if self.object.group_id:
            user_rezults = Student.objects.filter(active_group_id=self.object.group_id, ) \
                .annotate(user_rezult_pk=Subquery(all_users_rezults_subquery.values('pk')),
                          quize_started_it=Subquery(all_users_rezults_subquery.values('quize_started_it')))
            context['report_cart'] = user_rezults

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.action == 'List':
            if '_retake_quize' in self.request.POST:
                self.quize_type.objects.get(user__pk=self.request.POST.get('_retake_quize'),\
                                                  parent_id=self.object).delete()

        user = Student.objects.get(pk=self.request.POST.get('_retake_quize'))
        messages.success(self.request, (user.first_name + ' ' + user.last_name + ' was sented to retake a quize'))
        if self.quize_type == QuizeRezultDecepline:
            return redirect('teacher_urls:report_card_discipine_url', pk=self.object.pk)
        elif self.quize_type == QuizeRezultTopic:
            return redirect('teacher_urls:report_card_topic_url', pk=self.object.pk)

class ReportCardDetail(ReportCard):
    template_name = 'teacher/teacher_office/report_card_detail.html'
    quize_log_type = ''
    action = 'Detail'

    def get_context_data(self, **kwargs):
        context = super(ReportCard, self).get_context_data(**kwargs,)
        if self.quize_type.objects.filter(user__pk=self.kwargs['user_pk'], parent_id=self.object).exists():
            context['rezult'] = self.quize_type.objects.get(user__pk=self.kwargs['user_pk'], parent_id=self.object)
            context['log'] = self.quize_log_type.objects.filter(user_id=self.kwargs['user_pk'], parent_id=self.object.pk,
                                                                test_type=get_final_quize_status(self))
        return context







