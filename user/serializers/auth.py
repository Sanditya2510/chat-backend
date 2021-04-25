from django.contrib.auth import get_user_model

from rest_framework import (
    serializers, exceptions
) 
from rest_framework_jwt.settings import api_settings

User = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
        ]
    
    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError('User with this email is already registered')
        return email
    
    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if user.exists():
            raise serializers.ValidationError('Username already exists')
        return username

    def validate(self,data):
        pw = data.get('password')
        pw2 = data.get('password2')
        if pw!=pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

class LoginSerializer(serializers.Serializer):
    """
    Validates the email and password, raises 404 if either is not 
    found else return a new token
    """
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        """
        Checks whether a user with the given email and password exists
        :param data: Request Object
        """ 
        username = data.get('username')
        password = data.get('password')
        
        user_exists = User.objects.filter(username=username).exists()
        
        if not user_exists:
            raise exceptions.NotFound(
                'A user with this username was not found'
            )   

        user = User.objects.get(username=username)
        
        if not user.check_password(password):
            raise exceptions.NotFound(
                'A user with this username and password was not found.'
            )

        return data
