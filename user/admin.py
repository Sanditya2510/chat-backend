from django.contrib import admin

from .models.user import User
from .models.friend import (
    Friend, FriendRequest, 
)

admin.site.register([User, Friend, FriendRequest])