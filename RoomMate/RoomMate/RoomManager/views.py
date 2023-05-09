from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.

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
	return render (request=request, template_name="RoomManager/register.html", context={"register_form":form})

def settings(request):
    return render(request, 'RoomManager/settings.html')

def room_booking(request):
    return render(request, 'RoomManager/room_booking.html')

def profile(request):
    return render(request, 'RoomManager/profile.html')