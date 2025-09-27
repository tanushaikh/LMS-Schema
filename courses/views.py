from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg
from accounts.models import User
from accounts.permissions import HasModelPermission
from django.db import IntegrityError



from .models import Course, Meeting, CourseEnrollment
from .serializers import CourseSerializer, MeetingSerializer, CourseEnrollmentSerializer




class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [HasModelPermission]

    app_label = "courses"
    model_name = "course"

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
        try:
            self.perform_destroy(instance)
            return Response(
                {"message": "Course deleted successfully"},
                status=status.HTTP_200_OK
            )
        except IntegrityError as e:
            return Response(
                {"error": "Cannot delete this course because it has related objects (Meetings/Enrollments)."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"], url_path="total")
    def total_courses(self, request):
        total = Course.objects.count()
        return Response({"total_courses": total}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="average-score")
    def average_score(self, request):
        avg_score = Course.objects.aggregate(avg=Avg("score"))["avg"] or 0
        percentage = round(avg_score, 2)
        return Response({"average_score": f"{percentage}%"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="average-learning-time")
    def average_learning_time(self, request):
        avg_minutes = Course.objects.aggregate(avg=Avg("duration_minutes"))["avg"] or 0
        hours = int(avg_minutes // 60)
        minutes = int(avg_minutes % 60)
        return Response({"average_learning_time": f"{hours}h {minutes}m"}, status=status.HTTP_200_OK)

# -------------------------------
# MEETING VIEWSET
# -------------------------------
import logging
logger = logging.getLogger(__name__)  # create logger instance


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [HasModelPermission]

    app_label = "courses"
    model_name = "meeting"

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
        meeting = serializer.save(user=self.request.user)
        logger.info(f"Meeting created successfully (ID={meeting.id}) by user={self.request.user}")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            logger.info(f"Meeting deleted successfully (ID={instance.id}) by user={request.user}")
            return Response({"message": "Meeting deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to delete meeting (ID={instance.id}) by user={request.user}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'title' not in data or not data['title']:
            logger.warning(f"Create meeting failed - missing title (user={request.user})")
            return Response({"title": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if 'meeting_link' not in data or not data['meeting_link']:
            logger.warning(f"Create meeting failed - missing meeting_link (user={request.user})")
            return Response({"meeting_link": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(f"Meeting created successfully with title='{serializer.data.get('title')}' by user={request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create meeting (user={request.user}): {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# COURSE ENROLLMENT VIEWSET
# -------------------------------
class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [HasModelPermission]

    app_label = "courses"
    model_name = "courseenrollment"

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
        try:
            self.perform_destroy(instance)
            return Response({"message": "Course enrollment deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
