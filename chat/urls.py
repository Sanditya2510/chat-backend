from django.urls import path

from chat.views.chat import ChatView

urlpatterns = [
    path('<username>/', ChatView.as_view())
]