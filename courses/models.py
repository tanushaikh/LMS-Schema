from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from accounts.models import User
class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    level  = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    students = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    progress = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    skills = models.JSONField(default=list)
    next_lesson = models.CharField(max_length=200)
    completed_lesson = models.IntegerField()
    total_lessons = models.IntegerField()
    certificate_status  = models.BooleanField(default=True)
    description = models.TextField()
    ai_assisted = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Course.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"course {self.pk}"

class Meeting(models.Model):
    host = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
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



class CourseEnrollment(models.Model):
    user = models.ForeignKey("accounts.User",  on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
