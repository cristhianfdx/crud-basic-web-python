"""Employee ViewSets"""

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer

GENERIC_ERROR = 'GENERIC_ERROR'
EMAIL_DUPLICATE_ERROR = 'duplicate key value violates unique constraint "employee_email_key'
DOCUMENT_NUMBER_DUPLICATE_ERROR = 'duplicate key value violates unique constraint "employee_document_number_key'
DEPARTMENT_NAME_DUPLICATE_ERROR = 'duplicate key value violates unique constraint "department_name_key'

SUCCESS_EMPLOYEE_CREATED_MESSAGE = 'El/La Emplead@ se ha creado correctamente'
SUCCESS_EMPLOYEE_DELETED_MESSAGE = 'El/La Emplead@ se ha eliminado correctamente'
SUCCESS_EMPLOYEE_UPDATED_MESSAGE = 'El/La Emplead@ se ha actualizado correctamente'

SUCCESS_DEPARTMENT_CREATED_MESSAGE = 'El Departamento se ha creado correctamente'
SUCCESS_DEPARTMENT_DELETED_MESSAGE = 'El Departamento se ha eliminado correctamente'

error_messages = {
    EMAIL_DUPLICATE_ERROR: 'El email ingresado ya se encuentra registrado.',
    DOCUMENT_NUMBER_DUPLICATE_ERROR: 'El número de documento ingresado ya se encuentra registrado.',
    GENERIC_ERROR: 'En este momento estamos presentando fallas, por favor intente más tarde.',
    DEPARTMENT_NAME_DUPLICATE_ERROR: 'El nombre ingresado ya se encuentra registrado.'
}


def get_error(error_code):
    if EMAIL_DUPLICATE_ERROR in error_code:
        return error_messages.get(EMAIL_DUPLICATE_ERROR)

    if DOCUMENT_NUMBER_DUPLICATE_ERROR in error_code:
        return error_messages.get(DOCUMENT_NUMBER_DUPLICATE_ERROR)

    if DEPARTMENT_NAME_DUPLICATE_ERROR in error_code:
        return error_messages.get(DEPARTMENT_NAME_DUPLICATE_ERROR)

    return error_messages.get(GENERIC_ERROR)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request, *args, **kwargs):
        department_request = request.data

        try:
            department = Department.objects.create(name=department_request['name'])

            department.save()
            return Response({'msg': SUCCESS_DEPARTMENT_CREATED_MESSAGE}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response_error(e)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs['pk']
        try:
            departments = Department.objects.filter(name__contains=name.upper())
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return response_error(e)

    def destroy(self, request, *args, **kwargs):
        try:
            department = self.get_object()
            department.delete()
            return Response({'msg': SUCCESS_DEPARTMENT_DELETED_MESSAGE}, status=status.HTTP_200_OK)
        except Exception as e:
            return response_error(e)


def response_error(error):
    error_code = get_error(error.args[0])
    if error_code is None:
        return Response(
            {'error': get_error(GENERIC_ERROR)}, status=status.HTTP_417_EXPECTATION_FAILED
        )
    return Response({'error': error_code}, status=status.HTTP_417_EXPECTATION_FAILED)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def create(self, request, *args, **kwargs):
        employee_request = request.data

        try:
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
            return Response({'msg': SUCCESS_EMPLOYEE_CREATED_MESSAGE}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response_error(e)

    def destroy(self, request, *args, **kwargs):
        try:
            employee = self.get_object()
            employee.delete()
            return Response({'msg': SUCCESS_EMPLOYEE_DELETED_MESSAGE}, status=status.HTTP_200_OK)
        except Exception as e:
            return response_error(e)

    def update(self, request, *args, **kwargs):
        employee_request = request.data

        try:
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
            return Response({'msg': SUCCESS_EMPLOYEE_UPDATED_MESSAGE}, status=status.HTTP_200_OK)

        except Exception as e:
            return response_error(e)
