from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from apps.educational_materials.models import DisciplineAccess
from apps.students.api.permissions import IsAnonymous, IsStudent
from apps.students.api.serializers import StudentRegisterSerializer
from apps.students.core import get_student_aviable_materials, get_student_unaviable_diciplines, get_student_group


class StudentRegister(CreateAPIView):
    """
            регистрация студента.
            permissions:
            IsAnonymous, SystemQuide.front_registration==True
    """
    serializer_class = StudentRegisterSerializer
    permission_classes = (IsAnonymous, )

class DecipisnesCount(APIView):
    """
            view aviable and unaviable education material counts
            permissions:
            IsStudent,
    """
    permission_classes = (IsStudent,)

    def get(self, request):
        from rest_framework.reverse import reverse
        all_access = DisciplineAccess.objects.filter(group_id=get_student_group(self), parent_id__status=True, )
        aviable_materials = all_access.filter(discipline_access_end__gte=timezone.now(),
                                           discipline_access_start__lte=timezone.now(),).count()
        unaviable_materials = all_access.filter(discipline_access_end__lte=timezone.now(),).count()
        return Response({
            "aviable_materials " + str(aviable_materials): reverse('students_urls:materials_list', request=request, ),
            "unaviable_materials " + str(unaviable_materials): reverse('students_urls:deciplines_list_unaviable',
                                                                       request=request, ),
                        })


class MaterialList(ListAPIView):
    """
            отображает список materials.
            permissions:
            IsStudent,
    """
    permission_classes = (IsStudent, )
    status = True

    def get_queryset(self):
        if self.status:
            return get_student_aviable_materials(self, self.serializer_class.Meta.model)
        else:
            return get_student_unaviable_diciplines(self)

class MaterialDetail(RetrieveAPIView):
    """
            отображает detail material.
            permissions:
            IsStudent,
    """
    permission_classes = (IsStudent, )
    status = True

    def get_queryset(self):
        if self.status:
            return get_student_aviable_materials(self, self.serializer_class.Meta.model)
        else:
            return get_student_unaviable_diciplines(self)