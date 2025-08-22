from django.db import models
from courses.models import Meeting
from django.utils.text import slugify


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
