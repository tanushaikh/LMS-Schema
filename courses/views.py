
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from accounts.models import UserLog
from accounts.views import get_client_ip
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from .models import Course, Meeting, Session, CourseEnrollment
from .serializers import CourseSerializer, MeetingSerializer, SessionSerializer, CourseEnrollmentSerializer


# ----------- COURSE CRUD -----------
class CourseListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        
        if request.user.is_authenticated:
            recent_log_exists = UserLog.objects.filter(
                user=request.user,
                action="get all courses",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()

            if not recent_log_exists:
                UserLog.objects.create(
                    user=request.user,
                    action="get all courses",
                    ip_address=get_client_ip(request)
                )
        else:
            # Log as anonymous user
            recent_log_exists = UserLog.objects.filter(
                user=None,
                action="get all courses",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            
            if not recent_log_exists:
                UserLog.objects.create(
                    user=None,
                    action="get all courses",
                    ip_address=get_client_ip(request)
                )

        return Response(serializer.data)



    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        
        if serializer.is_valid():
            # Log action
            if request.user.is_authenticated:
                recent_log_exists = UserLog.objects.filter(
                    user=request.user,
                    action=f"course create",
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()

                if not recent_log_exists:
                    UserLog.objects.create(
                        user=request.user,
                        action=f"course create",
                        ip_address=get_client_ip(request)
                    )
            else:
                # Log as anonymous user
                recent_log_exists = UserLog.objects.filter(
                    user=None,
                    action=f"anonymous course create",
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()

                if not recent_log_exists:
                    UserLog.objects.create(
                        user=None,
                        action=f"anonymous course create",
                        ip_address=get_client_ip(request)
                    )
           
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            # Log action
            if request.user.is_authenticated:
                recent_log_exists = UserLog.objects.filter(
                    user=request.user,
                    action=f"course detail update {pk}",
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()

                if not recent_log_exists:
                    UserLog.objects.create(
                        user=request.user,
                        action=f"course detail update {pk}",
                        ip_address=get_client_ip(request)
                    )
            else:
                # Log as anonymous user
                recent_log_exists = UserLog.objects.filter(
                    user=None,
                    action=f"anonymous course detail update {pk}",
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()

                if not recent_log_exists:
                    UserLog.objects.create(
                        user=None,
                        action=f"anonymous course detail update {pk}",
                        ip_address=get_client_ip(request)
                    )

            # ✅ Save the updated course after logging
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()

        # Log action
        if request.user.is_authenticated:
            recent_log_exists = UserLog.objects.filter(
                user=request.user,
                action=f"delete course {pk}",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()

            if not recent_log_exists:
                UserLog.objects.create(
                    user=request.user,
                    action=f"delete course {pk}",
                    ip_address=get_client_ip(request)
                )
        else:
            # Log as anonymous user
            recent_log_exists = UserLog.objects.filter(
                user=None,
                action=f"anonymous delete course {pk}",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()

            if not recent_log_exists:
                UserLog.objects.create(
                    user=None,
                    action=f"anonymous delete course {pk}",
                    ip_address=get_client_ip(request)
                )

        return Response(
            {"message": "Course deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ----------- MEETING CRUD -----------
class MeetingListCreateView(APIView):
    def get(self, request):
        meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeetingDetailView(APIView):
    def get(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    def put(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        meeting.delete()
        return Response({"message": "Meeting deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----------- SESSION CRUD -----------
class SessionListCreateView(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionDetailView(APIView):
    def get(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    def put(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        serializer = SessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        session.delete()
        return Response({"message": "Session deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----------- COURSE ENROLLMENT CRUD -----------
class CourseEnrollmentListCreateView(APIView):
    def get(self, request):
        enrollments = CourseEnrollment.objects.all()
        serializer = CourseEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseEnrollmentDetailView(APIView):
    def get(self, request, pk):
        enrollment = get_object_or_404(CourseEnrollment, pk=pk)
        serializer = CourseEnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def put(self, request, pk):
        enrollment = get_object_or_404(CourseEnrollment, pk=pk)
        serializer = CourseEnrollmentSerializer(enrollment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        enrollment = get_object_or_404(CourseEnrollment, pk=pk)
        enrollment.delete()
        return Response({"message": "Enrollment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
