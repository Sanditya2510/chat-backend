from django.contrib.auth import get_user_model

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.permissions import IsOwner

from user.serializers.user import (
    UserProfileSerializer,
)

User = get_user_model()

class UserView(generics.RetrieveAPIView,
                mixins.UpdateModelMixin,):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = request.user
        res = {
            "first_name": user.first_name,
            "last_name": user.first_name,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
        }

        if user.bday:
            res["bday"] = user.bday

        if user.dp:
            res["dp"] = user.dp
        
        return Response(res, status=status.HTTP_200_OK)

class UserProfile(generics.RetrieveAPIView,
                mixins.UpdateModelMixin,):
    permission_classes = (IsAuthenticated, IsOwner, )
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    queryset = User.objects.all()    

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
