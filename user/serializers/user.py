from django.contrib.auth import get_user_model

from rest_framework import (
    serializers, 
) 

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'bday',
            'dp',
        ]

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'bio',
            'dp'
        ]

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'bio',
            'dp',
        ]