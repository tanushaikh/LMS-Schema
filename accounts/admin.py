
from django.contrib import admin
from .models import Role, Permission, RolePermission, User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_model', 'permission_type', 'slug')
    prepopulated_fields = {'slug': ('app_model',)}

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'slug')

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'slug',)}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'mobile', 'country', 'slug')
    search_fields = ('user__username', 'full_name', 'mobile')
