from django.contrib import admin
from django.urls import path
from chat.views import gemini_chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', gemini_chat),
]
