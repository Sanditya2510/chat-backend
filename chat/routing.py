from django.urls import re_path

from chat.consumers.chat import ChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/grp/(?P<id>\w+)/$', GroupChatConsumer.as_asgi()),
]
