from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('room_booking/', views.room_booking, name='room_booking'),
]