from django.urls import path

from chat.views.chat import (
    ChatView, UserChatView,
    GroupThreadView,
    GroupThreadDetailView,
)

urlpatterns = [
    path('', UserChatView.as_view()),
    path('<username>/', ChatView.as_view()),
    path('<username>/group/', GroupThreadView.as_view()),
    path('<username>/group/<id>/', GroupThreadDetailView.as_view()),
]