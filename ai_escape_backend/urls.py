# ai_escape_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),  # ✅ chat.urls를 include
    path('captcha-stage/', include('captcha_stage.urls')), # ✅ captcha_stage.urls를 include
]
