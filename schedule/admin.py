from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user','reminder_time')
    search_fields = ('user__username', 'session__title')
