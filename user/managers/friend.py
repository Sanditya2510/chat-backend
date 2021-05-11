from django.db import models
from django.db.models import Q

from django.contrib.auth import get_user_model 

User = get_user_model()

class FriendManager(models.Manager):
    def get_friends(self, user):
        qlookup = Q(user=user)|Q(friend=user)
        qs = self.get_queryset().filter(qlookup)
        return qs

    def are_friends(self, user1, user2):
        user1 = User.objects.get(username=user1)
        user2 = User.objects.get(username=user2)
        qlookup = Q(user=user1, friend=user2)|Q(friend=user1, user=user2)
        cnt = self.get_queryset().filter(qlookup).count()
        
        return cnt>0
        

class FriendRequestManager(models.Manager):
    def get_requests_sent(self, user):
        qlookup = Q(user_from=user)
        qs = self.get_queryset().filter(qlookup)
        return qs

    def get_requests_received(self, user):
        qlookup = Q(user_to=user)
        qs = self.get_queryset().filter(qlookup)
        return qs
