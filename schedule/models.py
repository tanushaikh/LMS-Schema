from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class Schedule(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reminder = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reminder_time = models.DateTimeField()
    type = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    participants = models.IntegerField()
    color = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # 👇 Add slug field
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "schedule"  # use title, fallback "schedule"
            unique_suffix = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_suffix}"

            # ensure uniqueness
            while Schedule.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.start_time})"
