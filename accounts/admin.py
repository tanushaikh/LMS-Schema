from django.contrib import admin
from .models import User, Role, Permission, RolePermission, Profile, UserLog, Post


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "ip_address", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("user__email", "action", "ip_address")
    ordering = ("-timestamp",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "user__email")
    list_filter = ("created_at",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_superuser", "is_staff", "is_active", "created_at")
    search_fields = ("email", "role__name")
    list_filter = ("is_superuser", "is_staff", "is_active", "created_at", "role")
    ordering = ("-created_at",)

    # Make sure role is editable in the form
    fieldsets = (
        (None, {
            "fields": ("email", "username", "password", "role")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "is_staff", "is_superuser"),
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("app_label", "model_name", "permission_type", "slug")
    search_fields = ("app_label", "model_name", "permission_type")

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "permission", "slug")
    search_fields = ("role__name", "permission__slug")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "mobile", "country")
    search_fields = ("user__email", "full_name", "mobile", "country")
