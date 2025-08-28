from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from accounts.serializers import RegisterSerializer, LoginSerializer,PostSerializer,RolePermissionSerializer,PermissionSerializer,RoleSerializer,ProfileSerializer
from accounts.models import UserLog, User,Post,RolePermission,Role,Permission,Profile
from datetime import timedelta
from django.utils import timezone
import logging
from rest_framework import viewsets, permissions,status
from rest_framework.permissions import IsAuthenticated
from lms.models import *
from django.db import transaction, DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from courses.models import *
from session_lms.models import *
from schedule.models import *
from achievements.models import *
from assignments.models import *

logger = logging.getLogger('lmsapp')
User = get_user_model()


def delete_user_safe(user_obj):
    try:
        with transaction.atomic():
            user_obj.delete()
    except DatabaseError as e:
        print("Warning: related tables missing, deleted user anyway:", e)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


class RegisterView(APIView):
    def get(self, request):
        user_obj = User.objects.all()
        serializer = RegisterSerializer(user_obj, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Avoid duplicate logs
            recent_log_exists = UserLog.objects.filter(
                user=user, action='register',
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            if not recent_log_exists:
                UserLog.objects.create(user=user, action='register', ip_address=get_client_ip(request))

            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        logger.info("Login API called")

        login_id = request.data.get("username")
        password = request.data.get("password")
        print(login_id, password)

        user = None

        user = authenticate(request, username=login_id, password=password)

        if user is None:
            try:
                u = User.objects.get(username=login_id)
                if u.check_password(password) and u.is_active:
                    user = u
            except User.DoesNotExist:
                pass

        if user:
            login(request, user)
            logger.info(f"Login successful for user: {user.username}")

            recent_log_exists = UserLog.objects.filter(
                user=user,
                action="login",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            if not recent_log_exists:
                UserLog.objects.create(user=user, action="login", ip_address=get_client_ip(request))

            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)

        logger.warning(f"Invalid login attempt for: {login_id}")
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    """
    Update, delete, or soft-delete user by ID.
    """

    def put(self, request, pk):
        user_obj = get_object_or_404(User, pk=pk)
        serializer = RegisterSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Log update
            if request.user.is_authenticated:
                recent_log_exists = UserLog.objects.filter(
                    user=request.user,
                    action='update_user',
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()
                if not recent_log_exists:
                    UserLog.objects.create(
                        user=request.user,
                        action='update_user',
                        ip_address=get_client_ip(request)
                    )

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_obj = get_object_or_404(User, id=id)
        user_identifier = user_obj.email or user_obj.username

        try:
            with transaction.atomic():
                # Models with `user`
                CourseEnrollment.objects.filter(user=user_obj).delete()
                AITutorInteraction.objects.filter(user=user_obj).delete()
                Analytics.objects.filter(user=user_obj).delete()
                Certificate.objects.filter(user=user_obj).delete()
                Achievement.objects.filter(user=user_obj).delete()
                Role.objects.filter(user=user_obj).delete()
                Post.objects.filter(user=user_obj).delete()
                Certificate.objects.filter(user=user_obj).delete()
                Assignment.objects.filter(created_by=user_obj).delete()
                Analytics.objects.filter(user=user_obj).delete()

                Meeting.objects.filter(host=user_obj).delete()
                Course.objects.filter(created_by=user_obj).delete()
                Schedule.objects.filter(user=user_obj).delete()
                Bookmark.objects.filter(user=user_obj).delete()
                Feedback.objects.filter(user=user_obj).delete()
                Discussion.objects.filter(user=user_obj).delete()

                user_obj.userlog_set.all().delete()
                if hasattr(user_obj, 'profile'):
                    user_obj.profile.delete()

                # Delete user
                user_obj.delete()

            # Logging
            if request.user.is_authenticated and request.user != user_obj:
                try:
                    UserLog.objects.create(
                        user=request.user,
                        action=f'delete_user: {user_identifier}',
                        model_name='User',
                        ip_address=get_client_ip(request)
                    )
                except Exception:
                    pass

            return Response(
                {'message': f'User {user_identifier} has been successfully deleted.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': f'Failed to delete user: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
   
   
    def soft_delete(self, request, id):
            """
            Soft delete user by setting is_active=False
            """
            user_obj = get_object_or_404(User, id=id)
            user_identifier = user_obj.email or user_obj.username

            user_obj.is_active = False
            user_obj.save()

            if request.user.is_authenticated and request.user != user_obj:
                recent_log_exists = UserLog.objects.filter(
                    user=request.user,
                    action='soft_delete_user',
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()
                if not recent_log_exists:
                    UserLog.objects.create(
                        user=request.user,
                        action=f'soft_delete_user: {user_identifier}',
                        model_name='User',
                        ip_address=get_client_ip(request)
                    )

            return Response(
                {'message': f'User {user_identifier} has been deactivated.'},
                status=status.HTTP_200_OK
            )

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -------------------------------
# ROLE VIEWSET
# -------------------------------
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# -------------------------------
# PERMISSION VIEWSET
# -------------------------------
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


# -------------------------------
# ROLE PERMISSION VIEWSET
# -------------------------------
class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]   # 🔓 Open access


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny] 