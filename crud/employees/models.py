"""Models."""

from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=5)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return self.first_name
