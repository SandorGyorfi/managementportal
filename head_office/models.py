from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager, Group, Permission
# Create your models here.
class DepartmentUser(AbstractUser):
    DEPARTMENTS = (
        ('head_office', 'Head Office'),
        ('customer_service', 'Customer Service'),
        ('financial_department', 'Financial Department'),
        ('delivery_department', 'Delivery Department'),
    )
    
    department = models.CharField(choices=DEPARTMENTS, max_length=50)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="departmentuser_set",
        related_query_name="departmentuser",
        help_text='The groups this department user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="departmentuser_set",
        related_query_name="departmentuser",
        help_text='Specific permissions for this department user.'
    )
    objects = DefaultUserManager()