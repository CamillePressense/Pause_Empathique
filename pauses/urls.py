from django.urls import path
from .views import dashboard, PauseCreateView, PauseFeelingUpdateView, PauseNeedUpdateView, PauseListView

urlpatterns = [
    path('dashboard/', view=dashboard, name='dashboard'),
    path('observation/', PauseCreateView.as_view(), name='observation'),
    path('<int:pause_id>/feelings/', PauseFeelingUpdateView.as_view(), name='feelings' ),
    path('<int:pause_id>/needs/', PauseNeedUpdateView.as_view(), name='needs'),
    path('diary/', PauseListView.as_view(), name='diary'),
]