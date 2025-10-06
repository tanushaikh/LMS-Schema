from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
import uuid
from courses.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=200)

    # optional fields
    instructor = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    priority = models.CharField(max_length=200, null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    earned_points = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)

    requirements = models.JSONField(default=list, blank=True)
    time_estimate = models.CharField(max_length=200, null=True, blank=True)
    ai_hints = models.JSONField(default=list, blank=True)
    feed_back = models.CharField(max_length=200, null=True, blank=True)
    submission_format = models.CharField(max_length=200, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    sumbitted_date = models.DateTimeField(null=True, blank=True)

    attachment = models.FileField(upload_to="assignments/", null=True, blank=True)

    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.created_by.username) if self.created_by.username else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Assignment.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=10, blank=True)
    feedback = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while AssignmentSubmission.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assignment.title if self.assignment else 'No Assignment'} - {self.user.username if self.user else 'Anonymous'}"