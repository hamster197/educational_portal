from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from apps.educational_materials.models import DisciplineAccess, TopicAccess
from apps.students.api.permissions import IsAnonymous, IsStudent
from apps.students.api.serializers import StudentRegisterSerializer
from apps.students.core import get_student_aviable_materials, get_student_unaviable_diciplines, get_student_group, \
    get_for_aviable_quize_access, get_quize_rezult
from apps.teachers.api.serializers import AllFieldsSerializer
from core.models import Student


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

class QuizeObject(RetrieveAPIView):
    now = timezone.now()
    quize_status = False
    model = None
    permission_classes = (IsStudent,)

    def setup(self, request, *args, **kwargs):
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if get_for_aviable_quize_access(self, ).filter(final_quize_start__lte=self.now, \
                                                       final_quize_end__gte=self.now).exists():
            self.quize_status = True

class QuizeApproval(QuizeObject):
    """
            view quize Approval.
            permissions:
            IsStudent,

    """

    def get_serializer_class(self):
        AllFieldsSerializer.Meta.model = self.model

        return AllFieldsSerializer
    def get_queryset(self):
        if self.model == DisciplineAccess:
            return get_for_aviable_quize_access(self, ).filter(parent_id__status=True)
        elif self.model == TopicAccess:
            return get_for_aviable_quize_access(self, ).filter(parent_id__status=True,
                                                                       parent_id__discipline_id__status=True,)

class QuizeRezult(QuizeApproval):
    """
            view quize rezult.
            permissions:
            IsStudent,
    """
    
    # def get_serializer_class(self):
    #     AllFieldsSerializer.Meta.model = self.model
    #
    #     return AllFieldsSerializer

    def get_queryset(self):
        return get_quize_rezult(self)



