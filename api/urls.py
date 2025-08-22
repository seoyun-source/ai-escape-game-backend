# backend-django/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('session/start', views.session_start, name='session_start'),
    path('session/state', views.session_state, name='session_state'),
    path('quiz/check',   views.quiz_check,    name='quiz_check'),
    path('sms/check',    views.sms_check,     name='sms_check'),
    path('key/reveal',   views.key_reveal,    name='key_reveal'),  # ✅ 추가
]
