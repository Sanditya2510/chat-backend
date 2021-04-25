from django.contrib.auth import get_user_model

from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from user.serializers.auth import (
    LoginSerializer,
    RegisterSerializer,
)

from user.utils import get_token

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

        res = get_token(user)

        return Response(res, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    """
    View for handling login related logic
    Returns:
        response: It consists of user info and token
    """
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        username=request.data.get('username')
        password=request.data.get('password')

        user = User.objects.get(username=username)

        res = get_token(user)

        return Response(res, status=status.HTTP_201_CREATED)
