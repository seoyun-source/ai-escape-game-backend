# security/game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tablet', views.tablet_page, name='tablet'),               # tablet
    path('api/check-answer', views.check_answer, name='check'),     # API
    path('start_2/', views.start_2, name='start_2'),
    path('transition/', views.transition, name='transition'),
    path("opendoor/", views.opendoor, name="opendoor"),
    path("classroom/", views.classroom_scene, name="classroom"), 
    path("classroom/tablet_message.html", views.tablet_message, name="tablet_message"),
    path("classroom/chalkboard_hint.html", views.chalkboard_hint, name="chalkboard_hint"),
    path("classroom/hint.html", views.hint, name="hint"),
    path("home/", views.home_screen, name="home"),
    path("home/decoder/", views.decoder_app, name="decoder"),

]
