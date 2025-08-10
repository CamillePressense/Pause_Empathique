from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView 
from .forms import CustomAuthenticationForm
from users.models import User

def home(request):
    return render(request, 'users/home.html')

""" def dashboard(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'users/dashboard.html', { 'user_profile' : user_profile}) """


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    #redirect_authenticated_user = True

