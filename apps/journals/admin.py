from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.journals.models import *

# Register your models here.
class DisciplineJournalAdmin(ModelAdmin):
    list_display = ('pk', 'creation_date', 'title', 'material_type', )
    list_filter = ('material_type', )
    search_fields = ('title', )
    search_help_text = 'введите Название обьекта или id для поиска'
    readonly_fields = ('title', 'action', 'material_type', )

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

admin.site.register(DisciplineJournal, DisciplineJournalAdmin)

class QuestionsCopyJournalAdmin(ModelAdmin):
    list_display = ('pk', 'creation_date', 'author', 'action', 'from_theme', )
    list_filter = ('from_theme', )
    search_fields = ('author', )
    search_help_text = 'введите Login для поиска'
    readonly_fields = ('author', 'action', 'from_theme', )

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

admin.site.register(QuestionsCopyJournal, QuestionsCopyJournalAdmin)