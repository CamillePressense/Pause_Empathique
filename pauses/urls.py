from django.urls import path
from .views import (
    dashboard,
    delete_pause,
    PauseCreateView, 
    PauseFeelingUpdateView, 
    PauseNeedUpdateView,
    PauseUpdateView, 
    PauseListView)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('observation/', PauseCreateView.as_view(), name='observation'),
    path('<int:pause_id>/feelings/', PauseFeelingUpdateView.as_view(), name='feelings' ),
    path('<int:pause_id>/needs/', PauseNeedUpdateView.as_view(), name='needs'),
    path('diary/', PauseListView.as_view(), name='diary'),
    path('diary/<int:pause_id>/delete/', delete_pause, name='delete_pause'),
    path('diary/<int:pk>/update/', PauseUpdateView.as_view(), name='update_pause'),
]