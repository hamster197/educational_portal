from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.educational_materials.models import *

# Register your models here.

class TopicInline(admin.StackedInline):
    model = Topic

class DisciplineAdmin(ModelAdmin):
    inlines = [TopicInline, ]
    list_display = ('pk', 'creation_date', 'title', 'department_id', )
    list_filter = ('department_id', )
    search_fields = ('title', )
    search_help_text = 'введите Название дисциплины для поиска'
    readonly_fields = ['department_id', ]

admin.site.register(Discipline, DisciplineAdmin)

class ParentAccessAdmin(ModelAdmin):
    list_display = ('pk', 'group_id', 'parent_id', 'quiestion_quantity', 'time', )
    list_filter = ('parent_id', 'group_id',)
    search_help_text = 'введите Название материала для поиска'
    #readonly_fields = ['parent_id', ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(DisciplineAccess, ParentAccessAdmin)

admin.site.register(TopicAccess, ParentAccessAdmin)

class TopicMaterialInline(admin.StackedInline):
    model = TopicMaterial

class TopicVideoInline(admin.StackedInline):
    model = TopicVideo

class TopicAdmin(ModelAdmin):
    inlines = [TopicMaterialInline, TopicVideoInline]
    list_display = ('pk', 'creation_date', 'title', 'discipline_id', )
    list_filter = ('discipline_id', )
    search_fields = ('title', )
    search_help_text = 'Bведите Название Tемы для поиска'

admin.site.register(Topic, TopicAdmin)

class AnswerInline(admin.StackedInline):
    model = Answer
    readonly_fields = ('first_columnn', 'second_column', )

    def has_add_permission(self, request, obj):
        return False

class QuestionAdmin(ModelAdmin):
    def get_topics_access(self, obj):
        return "\n".join([p.title for p in obj.topic_access.all()])

    get_topics_access.short_description = 'Тема'

    inlines = [AnswerInline, ]
    list_display = ('pk', 'get_topics_access', 'variants_type', 'question_text', )
    list_filter = ('topic_access__title', )
    readonly_fields = ('topic_access', )
    search_fields = ('question_text', )
    search_help_text = 'Bведите текст вопроса для поиска'

admin.site.register(Question, QuestionAdmin)

