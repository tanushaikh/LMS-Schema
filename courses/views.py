from rest_framework import viewsets
from .models import Course, Meeting, Session, CourseEnrollment
from .serializers import (
    CourseSerializer,
    MeetingSerializer,
    SessionSerializer,
    CourseEnrollmentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer





class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
