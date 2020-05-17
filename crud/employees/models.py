"""Employee Model."""

from django.db import models


class Departament(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'departament'

    def __str__(self):
        return self.code


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=5)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return self.first_name
