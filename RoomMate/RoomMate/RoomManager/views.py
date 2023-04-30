from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')

def room_booking(request):
    return render(request, 'room_booking.html')