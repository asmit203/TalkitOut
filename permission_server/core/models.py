from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    MANAGER = 'MANAGER', 'Manager'
    EMPLOYEE = 'EMPLOYEE', 'Employee'
    GUEST = 'GUEST', 'Guest'

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.GUEST
    )
    department = models.CharField(max_length=100, blank=True)