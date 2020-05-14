"""Employee Model."""

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=40, unique=True)
    avatar = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return self.first_name