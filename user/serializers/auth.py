from django.contrib.auth import get_user_model

from rest_framework import (
    serializers, exceptions
) 

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

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
        
        return password

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs.get('refresh'))
        
        data = {'access': str(refresh.access_token)}
        return data