from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.configurations.jwt import SIMPLE_JWT 

from chat.serializers.chat import (
    ChatSerializer
)

from chat.models.chat import Message

User = get_user_model()

class UserChatView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.get_last_chat_for_user(user)

        return qs
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ChatView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def get_queryset(self):
        user1 = self.request.user
        user2 = User.objects.get(username=self.kwargs['username'])
        
        qs = Message.objects.get_all_msgs_for_users(user1, user2)

        return qs
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

