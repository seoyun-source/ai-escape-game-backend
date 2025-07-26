from django.urls import path
from .views import gemini_chat

urlpatterns = [
    path("chat/", gemini_chat, name="chat"),
]
