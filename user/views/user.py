from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.permissions import IsOwner

from user.serializers.user import (
    UserSerializer,
)

User = get_user_model()

class UserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "first_name": user.first_name,
            "last_name": user.first_name,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)
    