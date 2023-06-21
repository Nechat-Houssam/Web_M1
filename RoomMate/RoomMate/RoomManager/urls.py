from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("create_room/", views.create_room_request, name="create_room"),
    path("register/", views.register_request, name="register"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room_booking/', views.room_booking, name='room_booking'),
    path('create_event/', views.create_event, name='create_event'),
    path('fetch_events/', views.fetch_events, name='fetch_events'),
    path('fetch_events_profile/', views.fetch_events_profile, name='fetch_events_profile'),
    path('about/', views.about, name='about'),
    path('delete_event/',views.delete_event, name='delete_event'),
    path('create_event_request/', views.create_event_request, name='create_event_request'),
    path('user_role_reset/', views.user_role_reset, name='user_role_reset'),
    path('update_user_info/', views.update_user_info, name='update_user_info'),
    path('cityview/', views.cityview, name='cityview'),
    path('create_note/', views.create_note_request, name='create_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('user_requests', views.user_requests, name='user_requests'),
    path('answer_requests', views.answer_requests, name='answer_requests')
]