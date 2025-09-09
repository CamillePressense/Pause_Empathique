from django.contrib import admin
from .models import Pause, Feeling, Need


@admin.register(Pause)
class PauseAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ("feeling_family", "feminine_name", "masculine_name")
    ordering = ("feeling_family",)


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = ("need_family", "name")
    ordering = ("need_family",)
