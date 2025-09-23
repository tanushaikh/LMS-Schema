from django.db import models
from django.utils.text import slugify
import uuid
from django.utils.text import slugify
from django.db import models

class Achievement(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)  # required
    category = models.CharField(max_length=200, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    rarity = models.CharField(max_length=200, blank=True, null=True)
    is_unlocked = models.BooleanField(default=False)
    progress = models.IntegerField(blank=True, null=True)
    requirement = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    earned_on = models.DateTimeField(blank=True, null=True)
    unlocked_date = models.DateTimeField(blank=True, null=True)
    icon = models.ImageField(upload_to='achievements/', blank=True, null=True)

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
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, null=True, blank=True)
    issued_on = models.DateTimeField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Certificate.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)



class Analytics(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, null=True, blank=True)
    progress_percent = models.FloatField(blank=True, null=True)
    sessions_completed = models.IntegerField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) if self.user else "anon"
            unique_suffix = str(uuid.uuid4())[:8]  # 8-char random string
            self.slug = f"{base_slug}-{unique_suffix}"
            
            # Ensure slug is unique (extra safety)
            while Analytics.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:8]
                self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)
