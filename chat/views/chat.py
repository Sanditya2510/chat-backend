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

class ChatView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def get_queryset(self):
        user1 = self.request.user
        user2 = User.objects.get(username=self.kwargs['username'])

        qs = Message.objects.filter(thread__first=user1, thread__second=user2)\
        or Message.objects.filter(thread__first=user2, thread__second=user1) 

        return qs
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
