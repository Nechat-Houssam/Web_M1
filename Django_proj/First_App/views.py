from django.shortcuts import render

def login_page(request):

    return render(request, 'login.html')

def main_page(request):
  
    return render(request, 'main.html')

def admin_view(request):
  
    return render(request, 'admin.html')

def info_page(request):
    
    return render(request, 'info.html')