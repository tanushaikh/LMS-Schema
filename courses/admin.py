from django.contrib import admin
from .models import (
    Course,
    Meeting,
    Session,
    Assignment,
    AssignmentSubmission,
    CourseEnrollment
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

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'start_time', 'end_time', 'is_live')
    list_filter = ('is_live', 'course')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_by')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'user', 'submitted_at', 'grade')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_on', 'is_completed')

