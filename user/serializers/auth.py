import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model

from rest_framework import (
    serializers, exceptions
) 
from rest_framework_simplejwt.settings import api_settings

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

ACCESS_TOKEN_LIFETIME = api_settings.ACCESS_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = api_settings.REFRESH_TOKEN_LIFETIME


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration Serializer

    Raises:
        serializers.ValidationError: if any of the input dont meet the reqs.
    """
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
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    access_token_expiry = serializers.SerializerMethodField()
    refresh_token_expiry = serializers.SerializerMethodField()

    def get_access_token_expiry(self, obj):
        return datetime.datetime.now()+ACCESS_TOKEN_LIFETIME-datetime.timedelta(seconds=200)
    
    def get_refresh_token_expiry(self, obj):
        return datetime.datetime.now()+REFRESH_TOKEN_LIFETIME-datetime.timedelta(seconds=200)

    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if not user.exists():
            raise serializers.ValidationError('User doesn\'t exist')
        return username

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.get(username=username)
        
        if not user.check_password(password):
            raise serializers.ValidationError('User doesn\'t exist')
        
        return {}

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access_token_expiry = serializers.SerializerMethodField()

    def get_access_token_expiry(self, obj):
        return datetime.datetime.now()+ACCESS_TOKEN_LIFETIME-datetime.timedelta(seconds=200)

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        
        return value


