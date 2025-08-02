from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from lms_sessions.models import sessions


class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    note = models.TextField(blank=True)
    is_notified = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.session.title}-{self.reminder_time}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.session.title} reminder"

