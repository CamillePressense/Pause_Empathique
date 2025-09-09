from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "firstname",
        "created_at",
        "updated_at",
        "gender",
        "is_active",
    )
    ordering = ("email",)
