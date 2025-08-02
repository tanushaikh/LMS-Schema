from django.contrib import admin
from .models import (
    Role, Permission, RolePermission, User, Profile,
    Course, Session, Meeting, Assignment, AssignmentSubmission,
    AITutorInteraction, Achievement, Certificate, Analytics,
    Notification, Feedback, CourseEnrollment, Bookmark, Discussion
)

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Meeting)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(AITutorInteraction)
admin.site.register(Achievement)
admin.site.register(Certificate)
admin.site.register(Analytics)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(CourseEnrollment)
admin.site.register(Bookmark)
admin.site.register(Discussion)
