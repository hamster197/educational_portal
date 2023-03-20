
from django.urls import path, include

from apps.portal.views import *

app_name = 'portal_urls'

urlpatterns = [
    path('blog_list/', BlogList.as_view(), name='blog_list_url'),
    path('blog_detail/<slug>/', BlogDetail.as_view(), name='blog_detail_url'),
    path('api/v1/', include('apps.portal.api.urls'),)
]
