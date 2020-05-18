"""Employee ViewSets"""

from rest_framework import viewsets, mixins

from . import models
from . import serializers


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class EmployeeViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        queryset = models.Employee.objects.all()
        if self.action == 'list':
            queryset = models.Employee.objects.defer('created', 'modified').select_related('department')
        return queryset
