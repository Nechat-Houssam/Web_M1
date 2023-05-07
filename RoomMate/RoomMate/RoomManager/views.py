from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'RoomManager/home.html')

def login(request):
    return render(request, 'RoomManager/login.html')

def settings(request):
    return render(request, 'RoomManager/settings.html')

def room_booking(request):
    return render(request, 'RoomManager/room_booking.html')