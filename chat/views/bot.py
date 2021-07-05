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

class QueryView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')