from django.contrib import admin
from .models import Achievement, Certificate, Analytics

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'earned_on','points')
    search_fields = ('title', 'user__username')
    list_filter = ('earned_on',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'issued_on')
    search_fields = ('user__username', 'course__title')
    list_filter = ('issued_on',)

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress_percent', 'sessions_completed', 'last_active')
    search_fields = ('user__username', 'course__title')
    list_filter = ('last_active',)

