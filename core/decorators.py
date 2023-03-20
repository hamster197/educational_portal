from django.shortcuts import get_object_or_404

from apps.educational_materials.models import Discipline
from core.models import Teacher
from functools import wraps
from django.core.exceptions import PermissionDenied

def teachers_check(user, ):
    if user.groups.all().exists():
        return Teacher.objects.filter(pk=user.pk).exists()

def teacher_displine_access(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
      deaprtment_id = get_object_or_404(Teacher, username=request.user.username).deaprtment_id
      descipline_deaprtment = get_object_or_404(Discipline, pk=kwargs['discipine_pk']).department_id
      if deaprtment_id == descipline_deaprtment:
          return function(request, *args, **kwargs)
      else:
          raise PermissionDenied

  return wrap