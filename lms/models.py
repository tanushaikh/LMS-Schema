from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

from courses.models import Course


# AITutorInteraction
class AITutorInteraction(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL,null=True, blank=True,related_name='lms_ai_user')
    question = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)


# Notification
class Notification(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

# Feedback
class Feedback(models.Model):
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

# Bookmark
class Bookmark(models.Model):
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

# Discussion
class Discussion(models.Model):
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
