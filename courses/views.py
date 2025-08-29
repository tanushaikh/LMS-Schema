from rest_framework import viewsets
from rest_framework.response import Response
from .models import Course, Meeting, CourseEnrollment
from .serializers import (
    CourseSerializer,
    MeetingSerializer,
    CourseEnrollmentSerializer,
)
from rest_framework import status

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def destroy(self, request, *args, **kwargs):
        print('hai')
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Course delete successfully "},
            status=status.HTTP_200_OK
        )
    
class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
