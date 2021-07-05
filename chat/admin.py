from django.contrib import admin

from chat.models.chat import(
    Thread, Message,
    GroupThread
) 

admin.site.register([Thread, Message, GroupThread])
