from rest_framework import serializers
from .models import Achievement, Certificate, Analytics


class AchievementSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Achievement
        fields = "__all__"
        read_only_fields = ["slug"]


class CertificateSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Certificate
        fields = [
            "id",
            "user",
            "user_username",
            "course",
            "course_title",
            "issued_on",
            "certificate_file",
            "slug",
        ]


class AnalyticsSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Analytics
        fields = [
            "id",
            "user",
            "user_username",
            "course",
            "course_title",
            "progress_percent",
            "sessions_completed",
            "last_active",
            "slug",
        ]
