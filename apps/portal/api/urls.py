from rest_framework import routers

from apps.portal.api.views import BlogViewSet, BlogGaleryViewSet

router = routers.SimpleRouter()

router.register('portal_api_urls', BlogViewSet, basename='portal_api_urls')
router.register('portal_galery_api_urls', BlogGaleryViewSet, basename='portal_galery_api_urls')

app_name = 'portal_api_urls'

urlpatterns = []

urlpatterns += router.urls
