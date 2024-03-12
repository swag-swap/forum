from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm


def home_view(request):
    user_authenticated = request.user.is_authenticated
    return render(request, "home.html", {"user_authenticated": user_authenticated})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'post/register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()

    return render(request, 'post/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  
        else: 
            return render(request, 'post/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'post/login.html')    

def my_logout(request):
    auth_logout(request)
    return redirect('/')
