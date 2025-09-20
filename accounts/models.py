from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from django.utils import timezone


# -------------------------------
# USER MANAGER
# -------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        # Auto-assign Admin role
        admin_role, _ = Role.objects.get_or_create(
            name="Admin", defaults={"description": "Superuser role", "slug": "admin"}
        )
        extra_fields.setdefault("role", admin_role)

        return self.create_user(email, password, **extra_fields)


# -------------------------------
# ROLE MODEL
# -------------------------------
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------------
# PERMISSION MODEL
# -------------------------------
class Permission(models.Model):
    app_label = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    permission_type = models.CharField(max_length=10, choices=[
        ("add", "Add"),
        ("view", "View"),
        ("edit", "Edit"),
        ("delete", "Delete"),
    ])
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.app_label}-{self.model_name}-{self.permission_type}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.app_label}.{self.model_name} - {self.permission_type}"


# -------------------------------
# ROLE PERMISSION
# -------------------------------
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.role.name}-{self.permission.slug}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role.name} - {self.permission}"


# -------------------------------
# USER MODEL
# -------------------------------
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    learning_goal = models.CharField(max_length=255, blank=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.email)
            slug = base_slug
            counter = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def has_permission(self, app_label, model_name, perm_type):
        if self.is_superuser:
            return True
        return RolePermission.objects.filter(
            role=self.role,
            permission__app_label=app_label,
            permission__model_name=model_name,
            permission__permission_type=perm_type
        ).exists()

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return RolePermission.objects.filter(
            role=self.role,
            permission__app_label=app_label
        ).exists()

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        try:
            app_label, action_model = perm.split(".")
            action, model_name = action_model.split("_", 1)
        except ValueError:
            return False
        return self.has_permission(app_label, model_name, action)

    def __str__(self):
        return self.email


from django.utils.text import slugify

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.user.id}")
            slug = base_slug
            counter = 1
            # Check for uniqueness
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# -------------------------------
# PROFILE MODEL
# -------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
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
            self.slug = slugify(f"{self.user.email}-profile")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


# -------------------------------
# USER LOG
# -------------------------------
class UserLog(models.Model):
    user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email if self.user else 'Anonymous'} - {self.action} ({self.model_name})"

