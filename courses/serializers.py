from rest_framework import serializers
from .models import Course, Meeting, Session, CourseEnrollment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "category", "slug"]  # slug add kiya
        read_only_fields = ['slug', 'created_at']

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ['slug']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ['slug']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        read_only_fields = ['slug', 'enrolled_on']
