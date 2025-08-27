from rest_framework import serializers
from .models import Assignment, AssignmentSubmission


class AssignmentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ["slug"]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.ReadOnlyField(source="assignment.title")
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id",
            "assignment",
            "assignment_title",
            "user",
            "user_username",
            "submission_file",
            "submitted_at",
            "grade",
            "feedback",
            "slug",
        ]
        read_only_fields = ["slug", "submitted_at"]
