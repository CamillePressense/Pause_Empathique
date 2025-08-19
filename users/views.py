from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView 
from .forms import CustomAuthenticationForm, RegisterForm
from users.models import User
from django.contrib.auth import login
from django.conf import settings

def home(request):
    return render(request, 'users/home.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    #redirect_authenticated_user = True

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)            
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})

