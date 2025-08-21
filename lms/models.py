from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

from courses.models import Course
# Meeting
class Meeting(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lms_meeting_user')
    title = models.CharField(max_length=200)
    meeting_link = models.URLField()
    platform = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recorded = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# AITutorInteraction
class AITutorInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='lms_ai_user')
    question = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)


# Notification
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='lms_notifications_user')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

# Feedback
class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='lms_feedback_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

# Bookmark
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='lms_bookmark_user')
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

# Discussion
class Discussion(models.Model):
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='discussion_user')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
