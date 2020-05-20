import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud.settings')
import random

import django

django.setup()

from faker import Faker

fake = Faker(locale='es_MX')

from crud.employees.models import Department

departments = ['CONTABILIDAD', 'RRHH', 'SISTEMAS', 'MANTENIMIENTO']


def add_departament(name):
    departament = Department.objects.get_or_create(name=name)[0]
    departament.save()


def populate():
    for entry in departments:
        add_departament(entry)


if __name__ == '__main__':
    print('Populating data... Please wait.')
    populate()
    print('Populating complete!')
