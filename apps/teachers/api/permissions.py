from rest_framework import permissions

from core.models import Teacher


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and Teacher.objects.filter(pk=request.user.pk).exists():
            return True
        return False