from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.permissions import IsOwner

from user.serializers.friend import(
    FriendSerializer, FriendRequestSerializer, 
) 
from user.models.friend import (
    Friend, FriendRequest
)

User = get_user_model()

class FriendView(generics.ListCreateAPIView,):
    permission_classes = (IsAuthenticated, IsOwner, )
    serializer_class = FriendSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.get_friends(user)
    

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        friend_username = request.data.get('friend')
        friend = User.objects.get(username=friend_username)

        friend = Friend.objects.create(user=user, friend=friend)
        friend.save()

        return Response({'detail': 'friend successfully added'}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

class FriendRequestView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsOwner, )
    serializer_class = FriendRequestSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user

        friend_request_type = self.request.GET.get('type')

        qs = None
        if friend_request_type == "sent":
            qs = FriendRequest.objects.get_requests_sent(user)
        
        elif friend_request_type == "received":
            qs = FriendRequest.objects.get_requests_received(user)

        else:
            pass
        
        return qs

    def post(self, request, *args, **kwargs):
        user_from = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_to_username = request.data.get('user_to')
        user_to = User.objects.get(username=user_to_username)

        friend_request = FriendRequest.objects.create(user_from=user_from, user_to=user_to)
        friend_request.save()

        return Response({'detail': 'request sent!'}, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
