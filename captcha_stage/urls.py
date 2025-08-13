from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='captcha_index'),
    path('captcha-image/', views.generate_captcha, name='captcha_image'),
    path('check-captcha/', views.check_captcha, name='check_captcha'),
]
