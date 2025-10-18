from django.contrib import admin
from .models import (
    Course,
    Meeting,
    CourseEnrollment,
)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'is_published', 'created_at')
    search_fields = ('title', 'category')
    list_filter = ('is_published', 'category')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'host', 'start_time', 'end_time', 'recorded')
    list_filter = ('platform', 'recorded')



@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_on', 'is_completed')
