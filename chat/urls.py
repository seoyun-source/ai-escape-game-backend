from django.contrib import admin
from django.urls import path, include
from chat.views import check_flag  # ✅ 이 줄 추가!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),  # ✅ chat 앱의 API들은 여기
    path('check_flag/', check_flag, name='check_flag'),  # ✅ 함수로 직접 연결
]
