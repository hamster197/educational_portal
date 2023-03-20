from rest_framework import routers
from django.urls import path, include
from apps.teachers.api.views import *

router = routers.SimpleRouter()

router.register('discipline_published_api_urls', DisciplinePublishedViewSet, basename='discipline_published_api_urls')
router.register('discipline_unpublished_api_urls', DisciplineUnPublishedViewSet, basename='discipline_unpublished_api_urls')
router_discipline_access = routers.SimpleRouter()
router_discipline_access.register('discipline_access_api_urls', DisciplineAccessViewSet, basename='discipline_access_api_urls')

router_topic = routers.SimpleRouter()
router_topic.register('topic_api_urls', TopicViewSet, basename='topic_api_urls')

router_topic_video = routers.SimpleRouter()
router_topic_video.register('topic_video_api_urls', TopicVideoViewSet, basename='topic_video_api_urls')

router_topic_material = routers.SimpleRouter()
router_topic_material.register('topic_material_api_urls', TopicMaterialViewSet, basename='topic_material_api_urls')

router_topic_access = routers.SimpleRouter()
router_topic_access.register('topic_access_api_urls', TopicAccessViewSet, basename='topic_access_api_urls')


router_question = routers.SimpleRouter()
router_question.register('question', QuestionViewSet, basename='question_api_urls')

router_answer = routers.SimpleRouter()
router_answer.register('answer', AnswerViewSet, basename='answer_api_urls')

router_answer_sequence = routers.SimpleRouter()
router_answer_sequence.register('answer_sequence', AnswerSequenceViewSet, basename='answer_sequence_api_urls')

answer_compliance_fc = routers.SimpleRouter()
answer_compliance_fc.register('answer_compliance_fc', AnswerFirstColumnComplianceViewSet, basename='answer_compliance_fc_api_urls')

answer_compliance_sc = routers.SimpleRouter()
answer_compliance_sc.register('answer_compliance_sc', AnswerSecondColumnComplianceViewSet, basename='answer_compliance_sc_api_urls')

app_name = 'teachers_api_urls'

urlpatterns = [
    path('discipline/<int:discipline_id>/', include(router_topic.urls,)),
    path('discipline_access/<int:discipline_id>/', include(router_discipline_access.urls,)),

    path('topic/<int:topic_id>/', include(router_question.urls, )),
    path('topic_video/<int:topic_id>/', include(router_topic_video.urls, )),
    path('topic_material/<int:topic_id>/', include(router_topic_material.urls, )),
    path('topic_access/<int:topic_id>/', include(router_topic_access.urls,)),

    path('<int:topic_id>/questions/copy/', QuestionCopy.as_view(), name='question_copy_api_url'),

    path('topic/<int:topic_id>/question/<int:question_id>/', include(router_answer.urls,)),
    path('topic/<int:topic_id>/question_sequence/<int:question_id>/', include(router_answer_sequence.urls,)),

    path('topic/<int:topic_id>/answer_compliance_fc/<int:question_id>/', include(answer_compliance_fc.urls,)),
    path('topic/<int:topic_id>/answer_compliance_sc/<int:question_id>/', include(answer_compliance_sc.urls,)),

    path('topic/<int:topic_id>/questions/<int:question_id>/answer_compliance/new/', AnswerComplianceNew.as_view(),
         name='answer_compliance_new_api_url'),
]

urlpatterns += router.urls