from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
# from sessions.models import Course
import uuid
from courses.models import Course
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    priiority = models.CharField(max_length=200)
    points = models.IntegerField()
    earned_points = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    requirements = models.JSONField(default=list)
    time_estimate = models.CharField(max_length=200)
    ai_hints = models.JSONField(default=list)
    feed_back = models.CharField(max_length=200)
    submission_format = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    sumbitted_date = models.DateTimeField()
    attachments = models.FileField(upload_to='assignments/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='Assignment_user')
    slug = models.SlugField(unique=True, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(f"{self.title}-{self.course.id}")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='AssignmentSubmission_user')
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=10, blank=True)
    feedback = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # ✅ fix

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.assignment.title)
            # add random part
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.assignment.title} - {self.user.username}"
