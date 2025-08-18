from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='create_course_user')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # sirf jab slug empty ho tab generate karo
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Course.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"course {self.created_by.username}"

class Meeting(models.Model):
    host = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='meetings_hosted')
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

class Session(models.Model):
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recording_url = models.URLField()
    is_live = models.BooleanField(default=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class CourseEnrollment(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='course_enr_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
