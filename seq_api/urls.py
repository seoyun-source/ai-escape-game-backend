# seq_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('check-sequence/', views.check_sequence, name='check_sequence'),
    path('ping/', views.ping, name='ping'),  # 헬스체크용 (선택)
]
