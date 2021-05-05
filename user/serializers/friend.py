from rest_framework import (
    serializers, exceptions
)
from django.contrib.auth import get_user_model
from django.db.models import Q

from user.models.friend import(
    Friend, FriendRequest, 
) 
from user.serializers.user import UserPublicSerializer


User = get_user_model()

class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.CharField(write_only=True)
    friends = serializers.ListField(read_only=True)
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = '__all__'
    
    def validate_friend(self,  friend_username):
        friend = User.objects.get(username=friend_username)
        user = self.context.get('request').user
        
        if not friend:
            raise serializers.ValidationError('No user with this username found')

        qlookup = Q(user=user, friend=friend) | Q(user=friend, friend=user)
        qs = Friend.objects.filter(qlookup)

        if qs.exists():
            raise serializers.ValidationError('Already friend')

        return friend

class FriendRequestSerializer(serializers.ModelSerializer):
    user_from = UserPublicSerializer(read_only=True)
    user_to = serializers.CharField()

    class Meta:
        model = FriendRequest
        fields = '__all__'

    def validate_user_to(self, user_to_username):
        user_to = User.objects.get(username=user_to_username) 
        user_from = self.context.get('request').user

        if not user_to:
            raise serializers.ValidationError('No user with this username found')
        
        qlookup = Q(user_from=user_from, user_to=user_to)
        qs = FriendRequest.objects.filter(qlookup)

        if qs.exists():
            raise serializers.ValidationError('Request Already Sent')
        
        qlookup = Q(user_from=user_to, user_to=user_from)
        qs = FriendRequest.objects.filter(qlookup)

        if qs.exists():
            raise serializers.ValidationError('Request Already Received')
        
        

        qlookup = Q(user=user_from, friend=user_to) | Q(user=user_to, friend=user_from)
        qs = Friend.objects.filter(qlookup)

        if qs.exists():
            raise serializers.ValidationError('Already friends')

        return user_to