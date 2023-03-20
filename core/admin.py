from django.contrib import admin
from django import forms
from django.urls import path
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect
import csv
import io
import os
import environ
from pathlib import Path

from core.core import students_import_from_csv
from core.models import *

# Register your models here.
class SystemQuideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'feed_group_id', 'front_registration', )
    list_editable = ('front_registration',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(SystemQuide, SystemQuideAdmin)

class FacultyQuideAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    search_help_text = 'введите название факультета для поиска'

admin.site.register(FacultyQuide, FacultyQuideAdmin)

class DepartmentQuideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'faculty_id',)
    list_filter = ( 'faculty_id',)
    search_fields = ('name',)
    search_help_text = 'введите название кафедры для поиска'

admin.site.register(DepartmentQuide, DepartmentQuideAdmin)

class StudentGroupQuideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'faculty_id',)
    list_filter = ( 'faculty_id',)
    search_fields = ('name',)
    search_help_text = 'введите название группы для поиска'

admin.site.register(StudentGroupQuide, StudentGroupQuideAdmin)


class MainUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'last_name', 'first_name', 'patronymic', 'email', 'is_active',)
    list_filter = ('groups',)
    search_fields = ('username', 'email', 'last_name',)
    search_help_text = 'введите логин, email или фамилию для поиска'
    ordering = ('-pk',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'last_name','first_name','patronymic', 'email',  'is_active', 'is_staff',
                       'is_superuser', 'groups', )
        }),
    )

admin.site.register(MainUser, MainUserAdmin)

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class StudentAdmin(UserAdmin):

    def get_active_group(self, obj):
        if obj.active_group_id:
            return obj.active_group_id.name
        else:
            return None
    get_active_group.short_description = 'Группа(Активная)'

    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'get_active_group')
    search_fields = ('username', 'email', 'last_name',)
    search_help_text = 'введите логин, email или фамилию для поиска'
    list_filter = ('all_group_id',)
    ordering = ('-pk',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'last_name','first_name','patronymic', 'email',  'is_active',
                       'grade_book_number', 'active_group_id', 'all_group_id',)
        }),
    )

    change_list_template = 'core/csv_import/students_import.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('students-import-csv/', self.import_csv, name='import'),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            result_string = students_import_from_csv(csv_file)
            self.message_user(request, result_string)
            return redirect('/admin/core/student/')
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, 'core/csv_import/students_csv_form.html', payload
        )

admin.site.register(Student, StudentAdmin)

class TeacherAdmin(UserAdmin):
    def get_active_deaprtment_id(self, obj):
        if obj.deaprtment_id:
            return obj.deaprtment_id.name
        else:
            return None

    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'get_active_deaprtment_id')
    get_active_deaprtment_id.short_description = 'Кафедра(Активная)'
    list_filter = ('all_department_id',)
    search_fields = ('username', 'email', 'last_name',)
    search_help_text = 'введите логин, email или фамилию для поиска'
    ordering = ('-pk',)
    fieldsets = (
        (None, {
            'fields': ( 'username', 'password', 'last_name', 'first_name', 'patronymic', 'email', 'is_active',
                       'deaprtment_id', 'all_department_id', )
        }),
    )

admin.site.register(Teacher, TeacherAdmin)#