from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg
from accounts.permissions import HasModelPermission
from django.db import IntegrityError
from rest_framework.views import APIView
from .models import Course, Meeting, CourseEnrollment,CourseStreak
from .serializers import CourseSerializer, MeetingSerializer, CourseEnrollmentSerializer
from datetime import date, timedelta

class StudyPlanGenerator:
    def __init__(self, course, days: int = 7):
        """
        Initialize study plan generator.
        :param course: Course instance
        :param days: Number of days to split topics into
        """
        self.course = course
        self.days = days
        self.topics = course.skills if course.skills else []

    def generate_plan(self):
        if not self.topics:
            return {}

        topics_per_day = max(1, len(self.topics) // self.days)
        plan = {}
        start_date = date.today()

        for i in range(self.days):
            day_topics = self.topics[i * topics_per_day:(i + 1) * topics_per_day]
            if not day_topics:
                break
            plan[str(start_date + timedelta(days=i))] = day_topics

        return {
            "course": self.course.title,
            "week_plan": plan
        }

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
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

    app_label = "courses"
    model_name = "course"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="study-plan")
    def study_plan(self, request, pk=None):
        course = self.get_object()
        generator = StudyPlanGenerator(course, days=7)
        plan = generator.generate_plan()

        if not plan.get("week_plan"):
            return Response({"error": "No topics found for this course."}, status=400)

        return Response(plan, status=status.HTTP_200_OK)

class UserStreakAPIView(APIView):
    def get(self, request, *args, **kwargs):
        streak, _ = CourseStreak.objects.get_or_create(user=request.user)
        return Response({
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "last_active": streak.last_active
        }, status=status.HTTP_200_OK)

class CourseTotalAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "courses"
    model_name = "course"
    permission_type = "view"  # requires courses.view_course

    def get(self, request, *args, **kwargs):
        total = Course.objects.count()
        return Response({"total_courses": total}, status=status.HTTP_200_OK)


class CourseAverageScoreAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "courses"
    model_name = "course"
    permission_type = "view"

    def get(self, request, *args, **kwargs):
        avg_score = Course.objects.aggregate(avg=Avg("score"))["avg"] or 0
        percentage = round(avg_score, 2)
        return Response({"average_score": f"{percentage}%"}, status=status.HTTP_200_OK)


class CourseAverageLearningTimeAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "courses"
    model_name = "course"
    permission_type = "view" 

    def get(self, request, *args, **kwargs):
        avg_minutes = Course.objects.aggregate(avg=Avg("duration_minutes"))["avg"] or 0
        hours = int(avg_minutes // 60)
        minutes = int(avg_minutes % 60)
        return Response(
            {"average_learning_time": f"{hours}h {minutes}m"},
            status=status.HTTP_200_OK
        )
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

class StudentTotalHoursAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "courses"
    model_name = "meeting"
    permission_type = "view"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        meetings = Meeting.objects.filter(user=user, start_time__isnull=False, end_time__isnull=False)

        total_seconds = 0
        for meeting in meetings:
            total_seconds += (meeting.end_time - meeting.start_time).total_seconds()

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        return Response(
            {"total_meeting_time": f"{hours}h {minutes}m"},
            status=status.HTTP_200_OK
        )
