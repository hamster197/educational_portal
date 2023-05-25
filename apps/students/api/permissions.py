from rest_framework import permissions

from core.models import SystemQuide, Student


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated and SystemQuide.objects.get(pk=1).front_registration==True:
            return True
        return False

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and Student.objects.filter(pk=request.user.pk).exists():
            return True
        return False