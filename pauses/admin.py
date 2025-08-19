from django.contrib import admin
from .models import Pause, Feeling, Need

@admin.register(Pause)
class PauseAdmin(admin.ModelAdmin):
    list_display= ('user', 'created_at', 'updated_at')

admin.site.register(Feeling)
admin.site.register(Need)

