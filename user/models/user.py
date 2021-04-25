from django.db import models
from django.contrib.auth.models import AbstractUser

from user.managers.user import UserManager

class User(AbstractUser):
    """
    Custom User Model 
    """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()