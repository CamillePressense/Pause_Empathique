from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard/', view=dashboard, name='dashboard')
]