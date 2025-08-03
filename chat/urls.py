# chat/urls.py
from django.urls import path
from .views import gemini_chat, check_flag

urlpatterns = [
    path('chat/', gemini_chat, name='gemini_chat'),
    path('check_flag/', check_flag, name='check_flag'),
]
