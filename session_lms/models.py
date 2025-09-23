from django.db import models
from courses.models import Meeting
from django.utils.text import slugify
import uuid
from django.utils.text import slugify
from django.db import models

class Session(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        "accounts.User", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    instructor = models.CharField(max_length=200, blank=True, null=True)
    instructor_avatar = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    participants = models.IntegerField(blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    course_title = models.CharField(max_length=200, blank=True, null=True)
    topics = models.JSONField(default=list, blank=True, null=True)
    is_recorded = models.BooleanField(default=False)
    has_handouts = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=200, blank=True, null=True)
    meeting_list = models.JSONField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True)
    is_live = models.BooleanField(default=False)
    meeting = models.OneToOneField(
        Meeting, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Session.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"Session {self.pk}"
