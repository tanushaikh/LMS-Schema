from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'created_by')
    search_fields = ('title', 'course__title')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'user', 'submitted_at', 'grade')
    search_fields = ('assignment__title', 'user__username')
    list_filter = ('grade',)

