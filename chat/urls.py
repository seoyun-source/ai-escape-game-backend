from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),  # ✅ include 사용
    path('check_flag/', 'chat.views.check_flag', name='check_flag'),  # ✅ FLAG 검증 API
]
