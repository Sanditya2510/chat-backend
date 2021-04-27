from django.contrib.auth import get_user_model

from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers.auth import (
    RegisterSerializer,
)

User = get_user_model()

class RegisterView(viewsets.ModelViewSet):
    """
    Viewset for handling registration related logic
    Returns:
        response: It consists of user info and token
    """
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        user = User.objects.create(username=username,
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name)
        user.set_password(password)
        user.save()

        tokens = RefreshToken.for_user(user)

        res = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }

        return Response(res, status=status.HTTP_201_CREATED)
