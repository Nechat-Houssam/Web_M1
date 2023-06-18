from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("create_room/", views.create_room_request, name="create_room"),
    path("register/", views.register_request, name="register"),
    path('settings/', views.settings, name='settings'),
    path('room_booking/', views.room_booking, name='room_booking'),
    path('create_event/', views.create_event, name='create_event'),
    path('fetch_events/', views.fetch_events, name='fetch_events'),
    path('fetch_events_profile/', views.fetch_events_profile, name='fetch_events_profile'),
    path('oursite/', views.oursite, name='oursite'),
    path('delete_event/',views.delete_event, name='delete_event')

]