from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'reminder_time', 'is_notified')
    search_fields = ('user__username', 'session__title')
    list_filter = ('is_notified', 'reminder_time')

