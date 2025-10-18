from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from django.conf import settings

# -------------------------------
# COURSE MODEL
# -------------------------------
class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", null=True, blank=True
    )
    instructor = models.CharField(max_length=200, null=True, blank=True)
    level  = models.CharField(max_length=200, null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    students = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=200, null=True, blank=True)
    progress = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    score = models.FloatField(null=True, blank=True, default=0)
    next_lesson = models.CharField(max_length=200, null=True, blank=True)
    completed_lesson = models.IntegerField(null=True, blank=True, default=0)
    total_lessons = models.IntegerField(null=True, blank=True, default=0)
    certificate_status  = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    ai_assisted = models.BooleanField(default=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
            
            while Course.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"course {self.pk}"

# -------------------------------
# MEETING MODEL
# -------------------------------
class Meeting(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="meetings", null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meetings", null=True, blank=True
    )
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    meeting_link = models.URLField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    recorded = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.host.username) if self.host else "anon"
            unique_suffix = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
            while Meeting.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

# -------------------------------
# COURSE ENROLLMENT MODEL
# -------------------------------
class CourseEnrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments", null=True, blank=True
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments", null=True, blank=True)
    enrolled_on = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)     
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
            while CourseEnrollment.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

class CourseStreak(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="streak"
    )
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def update_streak(self):
        today = timezone.now().date()
        if self.last_active == today:
            return

        if self.last_active == today - timezone.timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.last_active = today
        self.save()

    def __str__(self):
        return f"{self.user.username} Streak: {self.current_streak}"
# -------------------------------
# COURSE PDF MODEL
# -------------------------------
class CoursePDF(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="pdfs"
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="course_pdfs/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


# -------------------------------
# RECENT DOWNLOAD MODEL
# -------------------------------
class RecentDownload(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="downloads"
    )
    pdf = models.ForeignKey(CoursePDF, on_delete=models.CASCADE, related_name="downloads")
    downloaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} downloaded {self.pdf.title}"

class WeeklyStatusTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_tasks")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="weekly_tasks")
    day = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=20, default="2h")
    status = models.CharField(
        max_length=20,
        choices=[("completed", "Completed"), ("in-progress", "In Progress"), ("pending", "Pending")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.day}: {self.title}"

# -------------------------------
# Mentors MODEL
# -------------------------------
class Mentors(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentors", null=True, blank=True
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    company  = models.CharField(max_length=200, null=True, blank=True)
    reviews = models.IntegerField(default=0)
    students = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=200, null=True, blank=True)
    sessions = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=200, null=True, blank=True)
    locations = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    expertise = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    specialties = models.JSONField(default=list, blank=True)
    achievements = models.JSONField(default=list, blank=True)
    education = models.CharField(max_length=200, null=True, blank=True)
    responseTime = models.CharField(max_length=200, null=True, blank=True)
    availablity = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    hourlyRate = models.FloatField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
            
            while Course.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"course {self.pk}"

