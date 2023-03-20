from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.portal.api.serializers import BlogSerializer, BlogListSerializer, BlogGalerySerializer
from apps.portal.models import Blog, BlogGalery


class BlogViewSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class BlogViewSet(ModelViewSet):
    """
        Перечисляет и редактирует посты блога.
        edit permissions:
        request.user.is_staff
        view - request.user
    """
    queryset = Blog.objects.all().order_by('id')
    pagination_class = BlogViewSetPagination

    def get_serializer_class(self):

        if 'pk' in self.kwargs:
            self.serializer_class = BlogSerializer
        else:
            self.serializer_class = BlogListSerializer
        return self.serializer_class

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        if self.request.user.is_staff:
            self.http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
        else:
            self.http_method_names = ['get', ]
        return request

class BlogGaleryViewSet(ModelViewSet):
    """
            Перечисляет и редактирует галерею постов блога.
            permissions:
            request.user.is_staff
    """
    queryset = BlogGalery.objects.all()#.order_by('id')
    permission_classes = (IsAdminUser,)
    serializer_class = BlogGalerySerializer
