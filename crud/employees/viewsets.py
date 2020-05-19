"""Employee ViewSets"""

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def create(self, request, *args, **kwargs):
        employee_request = request.data

        employee = Employee.objects.create(
            first_name=employee_request['first_name'],
            last_name=employee_request['last_name'],
            document_number=employee_request['document_number'],
            birth_date=employee_request['birth_date'],
            mobile_number=employee_request['mobile_number'],
            email=employee_request['email'],
            gender=employee_request['gender'],
            department=Department.objects.get(id=employee_request['department']),
        )

        employee.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        employee_request = request.data
        employee = self.get_object()
        employee.first_name = employee_request['first_name']
        employee.last_name = employee_request['last_name']
        employee.document_number = employee_request['document_number']
        employee.birth_date = employee_request['birth_date']
        employee.mobile_number = employee_request['mobile_number']
        employee.email = employee_request['email']
        employee.gender = employee_request['gender']
        employee.department = Department.objects.get(id=employee_request['department'])
        employee.save()
        return Response(status=status.HTTP_200_OK)
