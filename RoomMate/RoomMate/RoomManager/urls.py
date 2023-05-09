from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path("logout/", views.logout_request, name= "logout"),
    path("profile/", views.profile, name= "profile"),
    path("register", views.register_request, name="register"),
    path('settings/', views.settings, name='settings'),
    path('room_booking/', views.room_booking, name='room_booking'),
]