from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid

# -------------------------------
# COURSE MODEL
# -------------------------------
class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200, null=True, blank=True)
    level  = models.CharField(max_length=200, null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    students = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=200, null=True, blank=True)
    progress = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)
    score = models.FloatField(null=True, blank=True, default=0)
    next_lesson = models.CharField(max_length=200, null=True, blank=True)
    completed_lesson = models.IntegerField(null=True, blank=True, default=0)
    total_lessons = models.IntegerField(null=True, blank=True, default=0)
    certificate_status  = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    ai_assisted = models.BooleanField(default=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True, null=True)

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


# -------------------------------
# MEETING MODEL
# -------------------------------
class Meeting(models.Model):
    # 🔥 CHANGE: Ab Meeting ek Course se linked hai
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,  
        related_name="meetings",null=True, 
    blank=True
    )
    host = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    meeting_link = models.URLField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    recorded = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)


# -------------------------------
# COURSE ENROLLMENT MODEL
# -------------------------------
class CourseEnrollment(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="enrollments",null=True,blank=True)
    enrolled_on = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)     
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # UUID based slug since no title exists
            self.slug = f"enroll-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
