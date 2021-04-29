from django.urls import path

from chat.views.chat import (
    ChatView, UserChatView
)

urlpatterns = [
    path('', UserChatView.as_view()),
    path('<username>/', ChatView.as_view())
]