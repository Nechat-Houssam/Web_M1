from .forms import NewUserForm, RoomForm
from .models import User, UserProfile, Room, Event, EventRequest, EventInvite
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime, timedelta
import json, requests

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

def oursite(request):
    return render(request, 'RoomManager/oursite.html')

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
    events = Event.objects.filter(creator=user)
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
    print(request.user)
    print(event)
    print(event_request_exists)
    if event_request_exists: 
        print("oui")
        return JsonResponse({'already':True})
    else :
        print("non")
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
    if request.method == 'POST':
        user = request.user

        email = request.POST.get('email')
        password = request.POST.get('password')

        if email:
            user.email = email

        if password:
            user.set_password(password)
            
        user.save()
    else:
        pass
    
    return redirect("profile")

def dashboard(request):
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
    print(data)
    return render(request, 'RoomManager/dashboard.html', {'data': data})

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
    return render(request, 'RoomManager/dashboard.html', {'data': data})