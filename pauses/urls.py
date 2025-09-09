from django.urls import path
from .views import (
    dashboard,
    delete_pause,
    PauseCreateView,
    PauseFeelingCreateView,
    PauseNeedCreateView,
    PauseUpdateView,
    PauseFeelingUpdateView,
    PauseNeedUpdateView,
    PauseListView,
    PauseDetailView,
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("observation/", PauseCreateView.as_view(), name="observation"),
    path("<int:pk>/feelings/", PauseFeelingCreateView.as_view(), name="feelings"),
    path("<int:pk>/needs/", PauseNeedCreateView.as_view(), name="needs"),
    path("diary/", PauseListView.as_view(), name="diary"),
    path("diary/<int:pk>/", PauseDetailView.as_view(), name="pause_details"),
    path("diary/<int:pk>/delete/", delete_pause, name="delete_pause"),
    path("diary/<int:pk>/update/", PauseUpdateView.as_view(), name="update_pause"),
    path(
        "diary/<int:pk>/feelings/update/",
        PauseFeelingUpdateView.as_view(),
        name="update_feelings",
    ),
    path(
        "diary/<int:pk>/needs/update/",
        PauseNeedUpdateView.as_view(),
        name="update_needs",
    ),
]
