from django.db import models
from django.contrib.auth.models import AbstractUser

from user.managers.user import UserManager

def upload_dp(instance,filename):
    return "dp/{username}/{filename}".format(username=instance.username, filename=filename)
    

class User(AbstractUser):
    """
    Custom User Model 
    """
    username = models.CharField(max_length=63, unique=True)
    email = models.EmailField(max_length=63, unique=True)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    bio = models.TextField(max_length=127, blank=True)
    joined = models.DateField(auto_now_add=True)
    bday = models.DateField(blank=True, null=True)
    dp = models.ImageField(upload_to=upload_dp,null=True,blank=True)   

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    @property
    def owner(self):
        return self.username