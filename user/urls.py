from django.urls import path, include
from rest_framework import routers
from user.views.auth import(
    RegisterView, LoginView, RefreshView,
    ChangePasswordView,
) 
from user.views.user import(
    UserView, UserProfile, 
) 

from user.views.friend import(
    FriendView, FriendRequestView
) 

router = routers.DefaultRouter()

urlpatterns = [
    path('', UserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('profile/<username>/', UserProfile.as_view()),
    path('change_password/<username>/', ChangePasswordView.as_view()),
    path('<username>/friend/', FriendView.as_view()),
    path('<username>/friend_request/', FriendRequestView.as_view()),
]
