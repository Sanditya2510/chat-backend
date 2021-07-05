from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.configurations.jwt import SIMPLE_JWT 

from backend.permissions import IsOwner, IsRequestingSelf

from backend.exceptions import DoesntExistError, NotAuthorizedError

from chat.serializers.chat import (
    ChatSerializer, GroupThreadSerializer,
    GroupThreadDetailSerializer,
)

from chat.models.chat import (
    Message, GroupThread,

) 

User = get_user_model()

class UserChatView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.get_last_chat_for_user(user)

        return qs
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ChatView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def get_queryset(self):
        user1 = self.request.user
        user2 = User.objects.get(username=self.kwargs['username'])
        
        qs = Message.objects.get_all_msgs_for_users(user1, user2)

        return qs
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class GroupThreadView(generics.ListCreateAPIView, ):
    permission_classes = (IsAuthenticated, IsRequestingSelf, )
    serializer_class = GroupThreadSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user
        qs = user.grps_is_member_of.all()
        return qs

    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('name')
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        grp = GroupThread.objects.create(name=name, created_by=user)
        grp.save()

        grp.users.add(user)
        grp.admins.add(user)

        return Response({'detail': 'group created successfully'}, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

class GroupThreadDetailView(generics.RetrieveAPIView, 
                            mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated, IsRequestingSelf, )
    serializer_class = GroupThreadDetailSerializer
    lookup_field = 'id'
    lookup_field2 = 'username'

    def get_queryset(self):
        user = self.request.user
        qs = user.grps_is_member_of.all()
        return qs

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        req_user = request.user
        
        grp_id = kwargs.get(self.lookup_field)
        grp = GroupThread.objects.get(id=grp_id)

        if not req_user in grp.admins.all():
            raise  NotAuthorizedError("User is not the admin")        

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        users_q = self.request.query_params.get('users_q')
        admins_q = self.request.query_params.get('admins_q')
        
        name = request.data.get('name')
        
        if name:
            grp.name = name

        users = request.data.get('users')

        if users:
            if users_q == "add":
                for user in users:
                    try:
                        user_obj = User.objects.get(username=user)
                    except:
                        raise DoesntExistError("Invalid User")

                    grp.users.add(user_obj)

            elif users_q == "delete":
                for user in users:
                    try:
                        user_obj = User.objects.get(username=user)
                    except:
                        raise DoesntExistError("Invalid User")

                    grp.users.remove(user_obj)

        admins = request.data.get('admins')

        if admins:
            if admins_q == "add":
                for admin in admins:
                    try:
                        user_obj = User.objects.get(username=user)
                    except:
                        raise DoesntExistError("Invalid User")

                    grp.admins.add(user_obj)

            elif admins_q == "delete":
                for admin in admins:
                    try:
                        user_obj = User.objects.get(username=user)
                    except:
                        raise DoesntExistError("Invalid User")

                    grp.admins.remove(user_obj)
        grp.save()

        return Response({'detail': 'fields changed successfully'}, status=status.HTTP_200_OK)

