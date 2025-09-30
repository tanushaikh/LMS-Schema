from rest_framework import viewsets
from .models import Achievement, Certificate, Analytics
from .serializers import AchievementSerializer, CertificateSerializer, AnalyticsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from accounts.permissions import HasModelPermission
from django.utils.text import slugify
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from courses.models import CourseEnrollment
from assignments.models import AssignmentSubmission

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by("-earned_on")
    serializer_class = AchievementSerializer
    permission_classes = [HasModelPermission]

    @action(detail=False, methods=["get"], url_path="total")
    def total_achievement(self, request):
        total = Achievement.objects.count()
        return Response(
            {"total_achievement": total},
            status=status.HTTP_200_OK
        )
        
    app_label = "achievements"
    model_name = "achievement"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        post = serializer.save(user=user)
        if not post.slug:
            post.slug = slugify(f"{post.title}-{user.username}")
            post.save()
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Achievement deleted successfully"},
            status=status.HTTP_200_OK
        )

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("-issued_on")
    serializer_class = CertificateSerializer
    permission_classes = [HasModelPermission]

    app_label = "achievements"
    model_name = "certificate"
    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(
            {"message": "Certificate deleted successfully"},
            status=status.HTTP_200_OK
        )


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all().order_by("-last_active")
    serializer_class = AnalyticsSerializer
    permission_classes = [HasModelPermission]

    app_label = "achievements"
    model_name = "analytic"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Analytics deleted successfully"},
            status=status.HTTP_200_OK
        )

from accounts.permissions import HasModelPermission  # optional, if you want it elsewhere
from rest_framework.permissions import BasePermission


# -------------------------------
# Custom Permission for Weekly Analytics
# -------------------------------
class WeeklyAnalyticsPermission(BasePermission):
    """
    Permission class that checks if user has view permissions for:
    - CourseEnrollment
    - AssignmentSubmission
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Check permission for CourseEnrollment
        if not user.has_perm("courses.view_courseenrollment"):
            return False

        # Check permission for AssignmentSubmission
        if not user.has_perm("assignments.view_assignmentsubmission"):
            return False

        return True


# -------------------------------
# Weekly Analytics View
# -------------------------------
class WeeklyAnalyticsView(APIView):
    """
    Returns weekly performance analytics per course/subject
    based on assignment completion.
    """
    permission_classes = [WeeklyAnalyticsPermission]

    def get(self, request):
        user = request.user

        today = timezone.now().date()
        week_ago = today - timedelta(days=6)

        # Get all course enrollments of the user
        enrollments = CourseEnrollment.objects.filter(user=user)
        analytics_data = []

        for enrollment in enrollments:
            course = enrollment.course

            # Count total assignments submitted this week
            total_assignments = AssignmentSubmission.objects.filter(
                user=user,
                assignment__course=course,
                submitted_on__date__range=[week_ago, today]
            ).count()

            # Count completed assignments
            completed_assignments = AssignmentSubmission.objects.filter(
                user=user,
                assignment__course=course,
                submitted_on__date__range=[week_ago, today],
                status="completed"  # adjust according to your model field
            ).count()

            progress_percent = (completed_assignments / total_assignments * 100) if total_assignments else 0

            analytics_data.append({
                "course": course.title,
                "total_assignments": total_assignments,
                "completed_assignments": completed_assignments,
                "progress_percent": round(progress_percent, 2)
            })

        return Response({"weekly_analytics": analytics_data}, status=status.HTTP_200_OK)