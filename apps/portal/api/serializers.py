from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.portal.models import Blog, BlogGalery
from core.models import MainUser

class AuthorSerializer(ModelSerializer):

    class Meta:
        model = MainUser
        fields = ['pk', 'first_name', 'last_name', 'patronymic',]

class BlogGalerySerializer(ModelSerializer):

    class Meta:
        model = BlogGalery
        fields = ['pk', 'picture', ]

class BlogSerializer(ModelSerializer):
    galery_blog_id = BlogGalerySerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['creation_date', 'author', 'main_image', 'name', 'text', 'galery_blog_id']

class BlogListSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['creation_date', 'author', 'main_image', 'name', 'text', 'url']
        extra_kwargs = {
            'url': {'view_name': 'portal_urls:portal_api_urls-detail', 'lookup_field': 'pk'},
        }


