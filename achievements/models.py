from django.db import models
from django.utils.text import slugify
import uuid

class Achievement(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='ach_Achievement_user')
    title = models.CharField(max_length=200)
    description = models.TextField()
    earned_on = models.DateTimeField()
    icon = models.ImageField(upload_to='achievements/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Achievement.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class Certificate(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='ach_Certificate_user')
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    issued_on = models.DateTimeField()
    certificate_file = models.FileField(upload_to='certificates/')
    slug = models.SlugField(unique=True)

class Analytics(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='ach_analytics_user')
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    progress_percent = models.FloatField()
    sessions_completed = models.IntegerField()
    last_active = models.DateTimeField()
    slug = models.SlugField(unique=True)
