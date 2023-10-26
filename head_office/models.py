from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager


# Create your models here.
class UserManager(DefaultUserManager):
    pass

class DepartmentUser(AbstractUser):
    DEPARTMENTS = (
        ('head_office', 'Head Office'),
        ('customer_service', 'Customer Service'),
        ('financial_department', 'Financial Department'),
        ('delivery_department', 'Delivery Department'),
    )
    
    department = models.CharField(choices=DEPARTMENTS, max_length=50)
    objects = UserManager()