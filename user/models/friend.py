from django.db import models
from django.contrib.auth import get_user_model

from user.managers.friend import (
    FriendManager, FriendRequestManager,
) 

User = get_user_model()

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    objects = FriendManager()

class FriendRequest(models.Model):
    user_from = models.ForeignKey(User, related_name='sent_by', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='received_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
 
    objects = FriendRequestManager()