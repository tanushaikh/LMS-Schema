from rest_framework import viewsets
from rest_framework.response import Response
from .models import Course, Meeting, CourseEnrollment
from .serializers import (
    CourseSerializer,
    MeetingSerializer,
    CourseEnrollmentSerializer,
)
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Avg

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Course delete successfully "},
            status=status.HTTP_200_OK
        )
    @action(detail=False, methods=["get"], url_path="total")
    def total_courses(self, request):
        total = Course.objects.count()
        return Response(
            {"total_courses": total},
            status=status.HTTP_200_OK
        )
    @action(detail=False, methods=["get"], url_path="average-score")
    def average_score(self, request):
        avg_score = Course.objects.aggregate(avg=Avg("score"))["avg"] or 0
        percentage = round(avg_score, 2)
        return Response(
            {"average_score": f"{percentage}%"},
            status=status.HTTP_200_OK
        )
    

    @action(detail=False, methods=["get"], url_path="average-learning-time")
    def average_learning_time(self, request):
        avg_minutes = Course.objects.aggregate(avg=Avg("duration_minutes"))["avg"] or 0
        hours = int(avg_minutes // 60)
        minutes = int(avg_minutes % 60)
        return Response(
            {"average_learning_time": f"{hours}h {minutes}m"},
            status=status.HTTP_200_OK
        )
class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
