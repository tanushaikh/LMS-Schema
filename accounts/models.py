from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Permission(models.Model):
    app_model = models.CharField(max_length=100)
    permission_type = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.app_model}-{self.permission_type}")
        super().save(*args, **kwargs)

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.role.name}-{self.permission.slug}")
        super().save(*args, **kwargs)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=False)  # User inactive until admin approves
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    full_name = models.CharField(max_length=150)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-profile")
        super().save(*args, **kwargs)