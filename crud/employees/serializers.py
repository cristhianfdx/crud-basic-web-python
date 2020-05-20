"""Serializers"""

from rest_framework import serializers

from .models import Employee, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'document_number',
            'birth_date',
            'mobile_number',
            'email',
            'gender',
            'department'
        )
        depth = 1
