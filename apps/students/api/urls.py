from django.urls import path, include

from apps.portal.api.views import BlogViewSetPagination
from apps.students.api.serializers import DisciplinesSerializer, DisciplineSerializer, TopicAccessDetailSerializer
from apps.students.api.views import *

urlpatterns = [
    path('sign_in/', StudentRegister.as_view(),),

    path('deciplines/main/', DecipisnesCount.as_view(), ),
    path('deciplines/unaviable/', MaterialList.as_view(status=False, serializer_class=DisciplinesSerializer,
                                                          pagination_class=BlogViewSetPagination),
         name='deciplines_list_unaviable'),
    path('deciplines/aviable/', MaterialList.as_view(serializer_class=DisciplinesSerializer,
                                                          pagination_class=BlogViewSetPagination), name="materials_list"),
    path('decipline/<int:pk>/', MaterialDetail.as_view(serializer_class=DisciplineSerializer),
         name='discipline_detail', ),
    path('topic/<int:pk>/', MaterialDetail.as_view(serializer_class=TopicAccessDetailSerializer), name='topic_detail', ),

    path('decepline/quize/approval/<int:pk>/', QuizeApproval.as_view(model=DisciplineAccess),
         name='decepline_quize_approval_url'),
    path('topic/quize/approval/<int:pk>/', QuizeApproval.as_view(model=TopicAccess), name='topic_quize_approval_url'),

    path('decepline/quize/rezult/<int:pk>/', QuizeRezult.as_view(model=DisciplineAccess),
         name='decepline_quize_rezult_url'),
    path('topic/quize/rezult/<int:pk>/', QuizeRezult.as_view(model=TopicAccess), name='topic_quize_rezult_url'),

]

