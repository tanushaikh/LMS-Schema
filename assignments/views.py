from rest_framework import viewsets, permissions
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by("-id")
    serializer_class = AssignmentSerializer
    permission_classes = []  # 🔓 No authentication

    def perform_create(self, serializer):
        # ✅ Don’t override, let client pass created_by
        serializer.save()

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by("-submitted_at")
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = []  # 🔓 No authentication

    def perform_create(self, serializer):
        serializer.save()  # let client send "user" field
