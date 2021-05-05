from django.db import models
from django.db.models import Q

class FriendManager(models.Manager):
    def get_friends(self, user):
        qlookup = Q(user=user)|Q(friend=user)
        qs = self.get_queryset().filter(qlookup)
        return qs

class FriendRequestManager(models.Manager):
    def get_requests_sent(self, user):
        qlookup = Q(user_from=user)
        qs = self.get_queryset().filter(qlookup)
        print(qs)
        return qs

    def get_requests_received(self, user):
        qlookup = Q(user_to=user)
        qs = self.get_queryset().filter(qlookup)
        return qs
