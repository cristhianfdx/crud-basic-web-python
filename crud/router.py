from rest_framework import routers

from .employees.viewsets import EmployeeViewSet, DepartmentViewSet

router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'department', DepartmentViewSet, basename='department')
