from django.urls import path, include
from rest_framework import routers
from user.views.auth import(
    RegisterView, LoginView, RefreshView,
    ChangePasswordView,
) 
from user.views.user import(
    UserView, UserProfile, 
    UserSearch, 
) 

from user.views.friend import(
    FriendView, FriendRequestView,
    DeleteFriendRequestView,
    UnfriendView, 
) 

router = routers.DefaultRouter()

urlpatterns = [
    path('', UserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('search/', UserSearch.as_view()),
    path('<username>/', UserProfile.as_view()),
    path('<username>/change_password', ChangePasswordView.as_view()),
    path('<username>/friend/', FriendView.as_view()),
    path('<username>/friend/<friend_id>/delete/', UnfriendView.as_view()),
    path('<username>/friend_request/', FriendRequestView.as_view()),
    path('<username>/friend_request/<friend_request_id>/delete/', DeleteFriendRequestView.as_view()),
]
