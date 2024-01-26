from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def homePage(request):
    return render(request, 'myapp/homePage.html')

from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success_page')
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


# def registerPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#         if(pass1!=pass2):
#             return HttpResponse('Password Not Matched')
#         else:
#             my_user=User.objects.create_user(username, email, pass1,first_name,last_name)
#             my_user.save()

#             return redirect( '/')
        
#     return render(request, 'myapp/signup.html')

