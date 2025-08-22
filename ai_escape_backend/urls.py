# ai_escape_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),  # ✅ chat.urls를 include
     path('captcha-stage/', include('seq_api.urls')),
       path('api/', include('api.urls')),  # ← 여기서만 'api/'를 붙입니다
]
