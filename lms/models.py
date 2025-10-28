from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

from courses.models import Course
import uuid
from django.utils.text import slugify
from django.db import models


# AITutorInteraction
class AITutorInteraction(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL,null=True, blank=True,related_name='lms_ai_user')
    question = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while AITutorInteraction.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)


# Notification
class Notification(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Notification.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

# Feedback
class Feedback(models.Model):
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Feedback.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

# Bookmark
class Bookmark(models.Model):
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Bookmark.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)


# Discussion
class Discussion(models.Model):
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Discussion.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    authorRole = models.CharField(max_length=150)
    publishDate = models.DateField()
    readTime = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    excerpt = models.TextField()
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    tags = models.JSONField(default=list)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs", null=True, blank=True
    )
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) if self.title else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Blog.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

from django.db import models

class ContactUs(models.Model):
    icon = models.URLField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    responseTime = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zipCode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contact", null=True, blank=True
    )
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) if self.title else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while ContactUs.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)


class FAQCategory(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Question(models.Model):
    category = models.ForeignKey(FAQCategory, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class LiveClass(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    format = models.CharField(max_length=50, default="live")
    students = models.IntegerField()
    maxStudents = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField()
    description = models.TextField()
    topics = models.JSONField()
    level = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class OnDemandClass(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    totalHours = models.CharField(max_length=50)
    format = models.CharField(max_length=50, default="on-demand")
    students = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField()
    description = models.TextField()
    topics = models.JSONField()
    level = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    completion = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    speakers = models.JSONField()
    price = models.CharField(max_length=50)
    attendees = models.IntegerField()

    def __str__(self):
        return self.title
