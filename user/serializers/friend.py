from rest_framework import (
    serializers, exceptions
)
from django.contrib.auth import get_user_model
from django.db.models import Q

from user.models.friend import(
    Friend, FriendRequest, 
) 
from user.serializers.user import UserPublicSerializer
from backend.exceptions import(
    NotAuthorizedError, DoesntExistError
) 

User = get_user_model()

class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.CharField()
    friends = serializers.ListField(read_only=True)
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = '__all__'
    
    def validate_friend(self,  friend_username):
        try:
            friend = User.objects.get(username=friend_username)
        except:
            raise DoesntExistError("User doesnt exist")

        user = self.context.get('request').user
        

        if not friend:
            raise serializers.ValidationError('No user with this username found')

        if user == friend:
            raise serializers.ValidationError('Can not add self as a friend')
            
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
        try:
            user_to = User.objects.get(username=user_to_username) 
        except:
            raise DoesntExistError("User doesnt exist")

        user_from = self.context.get('request').user

        if not user_to:
            raise serializers.ValidationError('No user with this username found')
        
        if user_to == user_from:
            raise serializers.ValidationError('Can not send a friend request to self')

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


class UnfriendSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context.get('request').user
        
        friend_id = self.context.get('id')
        
        try:
            friend_obj = Friend.objects.get(id=friend_id)
        except:
            raise DoesntExistError("Friendship doesnt exist")

        user1 = friend_obj.user
        user2 = friend_obj.friend

        if not (user == user1 or user == user2):
            raise NotAuthorizedError("you are not authorized to perform this request")

        return attrs
        

class DeleteFriendRequestSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context.get('request').user
        friend_request_id = self.context.get('id')

        try:
            friend_request_obj = FriendRequest.objects.get(id=friend_request_id)
        except:
            raise DoesntExistError("Friend Request doesnt exist")
    
        user_from = friend_request_obj.user_from
        user_to = friend_request_obj.user_to

        if not (user == user_from or user == user_to):
            raise NotAuthorizedError("you are not authorized to perform this request")
        
        return attrs
        