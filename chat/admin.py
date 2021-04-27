from django.contrib import admin

from chat.models.chat import Thread, Message

admin.site.register([Thread, Message])
