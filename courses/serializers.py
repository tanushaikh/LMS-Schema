from rest_framework import serializers
from .models import Course, Meeting, CourseEnrollment,WeeklyStatusTask,Mentors

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["slug"]

class MentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentors
        fields = "__all__"
        read_only_fields = ["slug"]

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ["slug"]

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = "__all__"
        read_only_fields = ["slug","user"]

from rest_framework import serializers
from .models import CoursePDF, RecentDownload

class CoursePDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePDF
        fields = "__all__"


class RecentDownloadSerializer(serializers.ModelSerializer):
    pdf_title = serializers.CharField(source="pdf.title", read_only=True)
    course_title = serializers.CharField(source="pdf.course.title", read_only=True)

    class Meta:
        model = RecentDownload
        fields = ["id", "user", "pdf", "pdf_title", "course_title", "downloaded_at"]
class WeeklyStatusTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyStatusTask
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
