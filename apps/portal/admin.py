from django.contrib import admin
from django.contrib.admin import ModelAdmin
from rangefilter.filters import DateRangeFilter

from apps.portal.models import *

class BlogGaleryInline(admin.TabularInline):
    model = BlogGalery

class BlogAdmin(ModelAdmin):
    list_display = ('pk', 'author', 'creation_date', 'name', 'slug',)
    list_filter = (('creation_date', DateRangeFilter), 'author__username',)
    inlines = [BlogGaleryInline, ]
    readonly_fields = ['slug', 'author']

# Register your models here.
admin.site.register(Blog, BlogAdmin)
