from django.db import models
from django.db.models import Q

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False

class MessageManager(models.Manager):
    def get_all_msgs_for_users(self, user1, user2):
        qlookup1 = Q(thread__first=user1) & Q(thread__second=user2)
        qlookup2 = Q(thread__first=user2) & Q(thread__second=user1)
        qs = self.get_queryset().filter(qlookup1 | qlookup2)
        return qs

    def get_last_chat_for_user(self, user):
        qs = (self.filter(thread__first=user) | self.filter(thread__second=user))\
            .order_by('thread', '-timestamp').distinct('thread')
        return qs