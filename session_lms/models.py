from django.db import models
from courses.models import Meeting
from django.utils.text import slugify


class Session(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.CharField(max_length=200)
    instructor_avatar = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    participants = models.IntegerField()
    max_participants = models.IntegerField()
    status = models.CharField(max_length=200)
    course_title = models.CharField(max_length=200)
    topics = models.JSONField(default=list)
    is_recorded = models.BooleanField(default=False)
    has_handouts = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=200)
    meeting_list = models.JSONField()
    content = models.TextField()
    description = models.TextField()
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
