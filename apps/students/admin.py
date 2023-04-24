from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.students.models import *

class QuizeAdmin(ModelAdmin):

    def get_estimation(self, obj):
        return obj.get_estimation()

    list_display = ('pk', 'user', 'parent_id', 'final_quize', 'ended_quize', 'get_estimation')
    list_filter = ('user', )
    search_fields = ('parent_id__parent_id__title', )
    search_help_text = 'введите Название дисциплины или темы для поиска'
    get_estimation.short_description = 'Оценка'
    readonly_fields = ('pk', 'user', 'parent_id', 'final_quize', 'ended_quize', 'get_estimation', 'quize_started_it',
                       'current_question', )

    def has_add_permission(self, request):
        return False

# Register your models here.

admin.site.register(QuizeRezultDecepline, QuizeAdmin)

admin.site.register(QuizeRezultTopic, QuizeAdmin)
