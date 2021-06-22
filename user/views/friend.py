from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.permissions import IsOwner, IsRequestingSelf

from user.serializers.friend import(
    FriendSerializer, FriendRequestSerializer, 
    DeleteFriendRequestSerializer, 
    UnfriendSerializer,
) 
from user.models.friend import (
    Friend, FriendRequest, 
)

User = get_user_model()

class FriendView(generics.ListCreateAPIView,):
    permission_classes = (IsAuthenticated, IsRequestingSelf)
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

class FriendRequestView(generics.ListCreateAPIView, ):
    permission_classes = (IsAuthenticated, IsRequestingSelf, )
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

class UnfriendView(generics.DestroyAPIView):
    serializer_class = UnfriendSerializer
    permission_classes = (IsAuthenticated, IsRequestingSelf, )
    lookup_field = 'friend_id'

    def delete(self, request, *args, **kwargs):
        friend_id = kwargs.get(self.lookup_field)
        
        context = {'request': request, 'id': friend_id}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        qs = Friend.objects.get(id=friend_id)
        
        qs.delete()

        return Response({'detail': 'successfully unfriended'}, status=status.HTTP_200_OK)


class DeleteFriendRequestView(generics.DestroyAPIView):
    serializer_class = DeleteFriendRequestSerializer
    permission_classes = (IsAuthenticated, IsRequestingSelf, )
    lookup_field = 'friend_request_id'

    def delete(self, request, *args, **kwargs):
        friend_request_id = kwargs.get(self.lookup_field)

        context = {'request': request, 'id': friend_request_id}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        friend_request = FriendRequest.objects.get(id=friend_request_id)
        friend_request.delete()

        return Response({'detail': 'request successfully deleted'}, status=status.HTTP_200_OK)
