from django.urls import path, include

from apps.teachers.views import *

app_name = 'teacher_urls'

urlpatterns = [
    path('', TeacherPersonalAccount.as_view(), name='personal_account_url'),
    path('change_data/', TeacherPersonalChange.as_view(), name='personal_account_change_url'),
    path('un_pub_discipline/', TeacherDiscipine.as_view(tab='tab2'), name='un_pub_discipline_url'),
    path('pub_discipline/', TeacherDiscipine.as_view(tab='tab3'), name='pub_discipline_url'),

    path('discipine/new/', DiscipineCreate.as_view(), name='discipline_new_url'),
    path('discipine/edit/<int:discipine_pk>/', DiscipineEdit.as_view(), name='discipline_edit_url'),
    path('discipine/edit/<int:discipine_pk>/new/', DisciplineAccessCreate.as_view(), name='discipline_access_new_url'),
    path('discipine/edit/<int:discipine_pk>/access/<int:pk>/', DisciplineAccessEdit.as_view(), name='discipline_access_edit_url'),

    path('discipine/topic/create/<int:discipine_pk>/', TopicCreate.as_view(), name='topic_create_url'),
    path('discipine/topic/edit/<int:pk>/', TopicEdit.as_view(), name='topic_edit_url'),
    path('discipine/topic/create/<int:discipine_pk>/access/<int:theme_pk>/', TopicAccessCreate.as_view(), name='topic_access_create_url'),
    path('discipine/topic/edit/<int:discipine_pk>/access/<int:pk>/', TopicAccessEdit.as_view(), name='topic_access_edit_url'),

    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/',
         QuestionsList.as_view(), name='question_list_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/edit/<int:pk>/',
         QuestionEdit.as_view(), name='question_edit_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/new/one/',
         QuestionCreate.as_view(action='one'), name='question_one_create_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/new/not_one/',
         QuestionCreate.as_view(action='not_one'), name='question_not_one_create_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/edit/sequence/<int:pk>/',
         QuestionSequenceEdit.as_view(), name='question_edit_sequence_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/edit/sequence/new/',
         QuestionSequenceComplianceCreate.as_view(question_type='Тест на последовательность'), name='question_new_sequence_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/edit/compliance/<int:pk>/',
         QuestionComplianceEdit.as_view(), name='question_edit_compliance_url'),
    path('discipine/topic/edit/<int:discipine_pk>/question_list/<int:topic_pk>/edit/compliance/new/',
         QuestionSequenceComplianceCreate.as_view(question_type='Тест на соответствие'), name='question_new_compliance_url'),

    path('api/v1/', include('apps.teachers.api.urls'),)
]