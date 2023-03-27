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

    #path('api/v1/', include('apps.teachers.api.urls'),)
]