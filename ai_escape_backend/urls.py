from django.contrib import admin
from django.urls import path
from chat.views import gemini_chat, check_flag  # ✅ 둘 다 import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', gemini_chat),         # ✅ AI 응답
    path('api/check_flag/', check_flag),    # ✅ FLAG 검증 API 추가!
]
