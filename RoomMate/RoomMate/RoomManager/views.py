from .forms import NewUserForm, RoomForm, EventForm
from .models import Room, Event
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'RoomManager/home.html')

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

def room_booking(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, 'RoomManager/room_booking.html', context)

def profile(request):
    return render(request, 'RoomManager/profile.html')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            event_data = {
                'creator_id': event.creator.id,
                'id': event.id,
                'date': event.date.strftime('%Y-%m-%d'),
                'start_time': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'end_time': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'room': {
                    'id': event.room.id,
                    'name': event.room.name,
                    'capacity': event.room.capacity,
                    'wing': event.room.get_wing_display(),
                    'floor': event.room.floor,
                    'number': event.room.number,
                }
            }
            return JsonResponse({'event': event_data})
        else:
            print(form.errors)
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = EventForm()
    return render(request, 'RoomManager/room_booking.html', {'form': form, 'rooms': Room.objects.all()})

def event_list(request):
    events = Event.objects.all()
    event_data = []

    for event in events:
        event_data.append({
            'title': event.room.name,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        })

    return JsonResponse(event_data, safe=False)

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