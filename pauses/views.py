from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pauses.models import Pause
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'pauses/dashboard.html', {'user': request.user} )


class PauseListView(LoginRequiredMixin, ListView):
    template_name = 'pauses/diary.html'
    model = Pause

class PauseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'pauses/pratice.html' 
    model = Pause
    fields = []
