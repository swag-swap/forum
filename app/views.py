from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Post

 
def homePage(request):
    user = request.user if request.user.is_authenticated else None

    all_posts = Post.objects.all()

    paginator = Paginator(all_posts, 5)   
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'user': user, 'posts': posts})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  
        else: 
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')