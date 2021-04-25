from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token 
from user.views.auth import RegisterView, LoginView

router = routers.DefaultRouter()
router.register(r'register', RegisterView, basename="user-register")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('refresh/', refresh_jwt_token),
]
