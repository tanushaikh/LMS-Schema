from django.contrib import admin
from .models import (AITutorInteraction,Notification, Feedback, Bookmark, Discussion )

admin.site.register(AITutorInteraction)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Bookmark)
admin.site.register(Discussion)