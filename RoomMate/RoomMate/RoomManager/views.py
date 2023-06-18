from .forms import NewUserForm, RoomForm, EventForm
from .models import Room, Event
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime, time, timedelta
from django.utils import timezone
import pytz

def home(request):
    rooms = Room.objects.all()
    return render(request, 'RoomManager/home.html', {'rooms': rooms})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password")
		else:
			messages.error(request,"Invalid username or password")
	form = AuthenticationForm()
	return render(request=request, template_name="RoomManager/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out") 
	return redirect("home")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful" )
			return redirect("home")
		messages.error(request, "Unsuccessful registration : invalid information")
	form = NewUserForm()
	return render(request=request, template_name="RoomManager/register.html", context={"register_form":form})


def create_room_request(request):
	if request.method == "POST":
		form = RoomForm(request.POST)
		if form.is_valid():
			room = form.save()
			messages.success(request, "Room creation successful" )
			return redirect("home")
		messages.error(request, "Unsuccessful room creation : invalid information")
	form = RoomForm()
	return render(request=request, template_name="RoomManager/create_room.html", context={"room_form":form})

def settings(request):
    return render(request, 'RoomManager/settings.html')

def profile(request):
    return render(request, 'RoomManager/profile.html')



def create_event(request):
    if request.method == 'POST':
        room_name = request.POST.get('room')
        day = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        st = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        et = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Ajout de 2 heures à l'objet datetime
        new_st = st + timedelta(hours=2)
        new_et = et + timedelta(hours=2)
        print(new_st)
        print(new_et)
        
        room = get_object_or_404(Room, name=room_name)

        event = Event(
            creator=request.user, 
            room=room,
            date=day,
            start_time=new_st,
            end_time=new_et
        )

        event.save()
        response_data = {
            'message': 'Événement créé avec succès',
        }
        return JsonResponse(response_data)
    else:
        pass


def delete_event(request, event_id):
    # Fetch the event object
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'DELETE':
        # Delete the event
        event.delete()
        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def room_booking(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        room_id = request.POST.get('room')
        room = get_object_or_404(Room, id=room_id)
        events = Event.objects.filter(room=room)
        return render(request, 'RoomManager/room_booking.html', {'rooms': rooms, 'events': events})

    return render(request, 'RoomManager/room_booking.html', {'rooms': rooms})


def fetch_events(request):
    room_id = request.GET.get('room_id')
    room = Room.objects.get(id=room_id)
    events = Event.objects.filter(room=room)

    event_data = []
    for event in events:
        event_data.append({
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        })

    return JsonResponse({'events': event_data})