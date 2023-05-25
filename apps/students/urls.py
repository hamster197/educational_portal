from django.urls import path, include

from apps.students.views import *

app_name = 'students_urls'

urlpatterns = [
    path('', StudentPersonalAccount.as_view(), name='st_personal_account_url'),
    path('change_data/', StudentPersonalChange.as_view(), name='st_personal_account_change_url'),
    path('discipline_aviable/', StudentDiscipines.as_view(tab='tab2'), name='discipline_aviable_url'),
    path('discipline_unaviable/', StudentDiscipines.as_view(tab='tab3'), name='discipline_unaviable_url'),
    path('discipline_detail/<int:pk>/', DiscipineDetail.as_view(), name='discipline_detail_url'),
    path('topic_detail/<int:pk>/', TopicDetail.as_view(), name='topic_detail_url'),

    path('decepline/quize/approval/<int:pk>/', QuizeApproval.as_view(model=DisciplineAccess),
         name='decepline_quize_approval_url'),
    path('topic/quize/approval/<int:pk>/', QuizeApproval.as_view(model=TopicAccess), name='topic_quize_approval_url'),

    path('decepline/quize/rezult/<int:pk>/', QuizeRezult.as_view(model=DisciplineAccess),
         name='decepline_quize_rezult_url'),
    path('topic/quize/rezult/<int:pk>/', QuizeRezult.as_view(model=TopicAccess), name='topic_quize_rezult_url'),

    path('decepline/quize/test/<int:pk>/', QuizeTest.as_view(model=DisciplineAccess),
         name='decepline_quize_test_url'),
    path('topic/quize/test/<int:pk>/', QuizeTest.as_view(model=TopicAccess), name='topic_quize_test_url'),

    path('api/v1/', include('apps.students.api.urls', ), )
]