from .forms import NewUserForm, RoomForm, NoteForm, UpdateUserInfoForm
from .models import User, UserProfile, Room, Event, EventRequest, EventInvite, Note
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
import json, requests
from django.utils import timezone

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

            profile = UserProfile(user=user, role='N')
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("home")
        messages.error(request, "Unsuccessful registration: invalid information")
    form = NewUserForm()
    return render(request=request, template_name="RoomManager/register.html", context={"register_form": form})

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

def profile(request):
    user = request.user
    return render(request, 'RoomManager/profile.html',{'user':user})

def about(request):
    rooms = Room.objects.all()
    return render(request, 'RoomManager/about.html', {'rooms': rooms})

def create_event(request):
    room_name = request.POST.get('room')
    day = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')

    st = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    et = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Ajout de 2 heures à l'objet datetime
    new_st = st + timedelta(hours=2)
    new_et = et + timedelta(hours=2)

        
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
        'message': 'Done',
    }
    return JsonResponse(response_data)

def room_booking(request):
    rooms = Room.objects.all()
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

def fetch_events_profile(request):
    user = request.user
    events = Event.objects.filter(Q(creator=user) | Q(invited__in=[user]))
    event_data = []
    for event in events:
        event_data.append({
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'room': event.room.name
        })
    return JsonResponse({'events': event_data})

def delete_event(request):
    start_time = request.POST.get('start_time')
    event = get_object_or_404(Event, start_time=start_time, creator=request.user)
    event.delete()
    return JsonResponse({'success': True})

def create_event_request(request):
    room_name = request.POST.get('room')
    room = get_object_or_404(Room, name=room_name)
    start_time = request.POST.get('start')
    event = get_object_or_404(Event, room=room, start_time=start_time)

    event_request_exists = EventRequest.objects.filter(to_event= event, from_profile= request.user).exists()
    if event_request_exists: 
        return JsonResponse({'already':True})
    else :
        EventRequest.objects.create(from_profile=request.user, to_event=event)
        return JsonResponse({'success':True})   

def user_role_reset(request):
    if request.user.is_superuser:
        profiles = UserProfile.objects.all()
        for profile in profiles:
            if not profile.user.is_superuser:
                profile.role = 'N'
                profile.save()

        users_without_profile = User.objects.filter(profile=None)
        for user in users_without_profile:
            UserProfile.objects.create(user=user, role='N')

        messages.success(request, "User roles have been reset")
    else:
        messages.error(request, "You do not have permission to reset user roles")

    return redirect("home")

def update_user_info(request):
    form = UpdateUserInfoForm(request.POST)
    if form.is_valid():
        user = request.user
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password'])
        
        new_username = form.cleaned_data['username']
        if new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                form.add_error('username', 'Username is already taken.')
                messages.error(request,"Username already taken")
                return redirect("profile")  
            user.username = new_username
            
        user.save()
        messages.info(request, 'Account information updated successfully.')
        updated_user = authenticate(username=user.username, password=form.cleaned_data['password'])
        login(request, updated_user)

        return redirect("profile")  

def dashboard(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Paris&APPID=f9c2f0f368afcfb53b6a73a394cfef82&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    if 'main' in data:
        data['main']['temp_parts'] = separate_temperature_parts(data['main']['temp'])
        data['main']['temp_min_parts'] = separate_temperature_parts(data['main']['temp_min'])
        data['main']['temp_max_parts'] = separate_temperature_parts(data['main']['temp_max'])
        data['main']['feels_like_parts'] = separate_temperature_parts(data['main']['feels_like'])
    else:
        data = None
    context = {
        'data': data,
        'notes': notes
    }
    return render(request, 'RoomManager/dashboard.html', context)

def separate_temperature_parts(temperature):
    temperature_str = str(temperature)
    if '.' in temperature_str:
        integer_part, decimal_part = temperature_str.split('.')
    else:
        integer_part = temperature_str
        decimal_part = '0'
    return {
        'integer_part': integer_part,
        'decimal_part': decimal_part,
    }

def cityview(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    city = request.POST.get('city')  # Retrieve the city name from the form
    print(city)
    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=f9c2f0f368afcfb53b6a73a394cfef82&units=metric'
        response = requests.get(url)
        data = json.loads(response.text)
        if 'main' in data:
            data['main']['temp_parts'] = separate_temperature_parts(data['main']['temp'])
            data['main']['temp_min_parts'] = separate_temperature_parts(data['main']['temp_min'])
            data['main']['temp_max_parts'] = separate_temperature_parts(data['main']['temp_max'])
            data['main']['feels_like_parts'] = separate_temperature_parts(data['main']['feels_like'])
        else:
            data = None
        print(data)
    else:
        data = None
    context = {
        'data': data,
        'notes': notes
    }
    return render(request, 'RoomManager/dashboard.html', context)

def create_note_request(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)  # Create Note object but don't save it yet
            note.user = request.user  # Set the user field to the currently logged-in user
            note.timestamp = timezone.now()  # Set the timestamp to the current date and time
            note.save()  # Save the note
            messages.success(request, "Note saved")
            return redirect("dashboard")
        messages.error(request, "Unsuccessful note saving: invalid information")
    form = NoteForm()
    return render(request, "RoomManager/create_note.html", {"note_form": form})

def edit_note(request, note_id):
    user = request.user
    note = get_object_or_404(Note, pk=note_id, user=user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'RoomManager/edit_note.html', {'note_form': form, 'note_id': note_id})

def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'RoomManager/edit_note.html', {'note_form': form, 'note_id': note_id})

def user_requests(request):
    user_events = Event.objects.filter(creator=request.user)
    user_requests = EventRequest.objects.filter(to_event__in=user_events, status=False)

    serialized_requests = []
    for request in user_requests:
        serialized_request = {
            'from_profile_username': request.from_profile.username,
            'to_event_start': request.to_event.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'to_event_room': request.to_event.room.name,
        }
        print(serialized_request)
        serialized_requests.append(serialized_request)

    json_data = json.dumps(serialized_requests)
    return JsonResponse({'requests': json_data})