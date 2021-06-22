from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings

from backend.permissions import IsOwner

from user.serializers.auth import (
    RegisterSerializer,
    LoginSerializer,
    RefreshSerializer,
    ChangePasswordSerializer,
)

from backend.utils import get_ws_token

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Viewset for handling registration related logic
    Returns:
        response: It consists of user info and token
    """
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
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

        return Response({'detail': 'user successfully created'}, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username)
        
        tokens = RefreshToken.for_user(user)

        ws_token = get_ws_token(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds(), user)
        
        access_token_expiry = serializer.data.get('access_token_expiry')
        refresh_token_expiry = serializer.data.get('refresh_token_expiry')

        res = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
            'ws_token': str(ws_token),
            'access_token_expiry': access_token_expiry,
            'refresh_token_expiry': refresh_token_expiry,
            'ws_token_token_expiry': access_token_expiry,
        }

        return Response(res, status=status.HTTP_201_CREATED)

    
class RefreshView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RefreshSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
            

        access_token_expiry = serializer.data.get('access_token_expiry')
        refresh =RefreshToken(serializer.data.get('refresh')) 
        
        access_token = str(refresh.access_token)
        ws_token = get_ws_token(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds(), user)

        res = {
            'access': access_token,
            'ws_token': ws_token,
            'access_token_expiry': access_token_expiry,
            'ws_token_token_expiry': access_token_expiry,
        }

        return Response(res, status=status.HTTP_201_CREATED)

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )
    serializer_class = ChangePasswordSerializer
    lookup_field = 'username'

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.user.username
        password = request.data.get('password')

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

        return Response({'detail: Password successfully updated'}, status=status.HTTP_200_OK)
