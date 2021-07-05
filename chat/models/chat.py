from django.db import models
from django.conf import settings
from django.db.models import Q

from chat.managers.chat import (
    ThreadManager, MessageManager
)

class Thread(models.Model):
    first = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='chat_thread_first')
    second = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = ThreadManager()

    @property
    def room_name(self):
        return f'chat_{self.id}'

class GroupThread(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='grps_is_member_of')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='grps_is_admin_of')
    name = models.CharField(max_length=63)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, 
                                    related_name='created_by')

    @property
    def room_grp_name(self):
        return f'grp_chat_{self.id}'
     

class Message(models.Model):
    thread = models.ForeignKey(Thread, null=True, 
                                blank=True, 
                                on_delete=models.SET_NULL)
    grp_thread = models.ForeignKey(GroupThread, null=True, 
                                    blank=True, 
                                    on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            verbose_name='sender', 
                            on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    objects = MessageManager()
