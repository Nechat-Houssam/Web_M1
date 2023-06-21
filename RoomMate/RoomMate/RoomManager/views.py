from .forms import NewUserForm, RoomForm, UpdateUserInfoForm
from .models import User, UserProfile, Room, Event, EventRequest, EventInvite
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

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

def settings(request):
    return render(request, 'RoomManager/settings.html')

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

@login_required
def update_user_info(request):
    if request.method == 'POST':
        form = UpdateUserInfoForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            updated_user = authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, updated_user)
            
            return redirect("profile")  
    else:
        pass
    
    return redirect("home")