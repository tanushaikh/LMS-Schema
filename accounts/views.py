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
from django.contrib.admin.models import LogEntry
from rest_framework.authtoken.models import Token
from accounts.models import UserLog
from django.db import connection
from accounts.utils import safe_delete_user
from .permissions import HasModelPermission
from rest_framework_simplejwt.tokens import RefreshToken

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
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            UserLog.objects.create(user=user, action="register", ip_address=get_client_ip(request))

            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import PermissionSerializer

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        login_id = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=login_id, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        refresh = RefreshToken.for_user(user)

        if not user.role:
            return Response({"error": "User does not have a role assigned"}, status=status.HTTP_400_BAD_REQUEST)

        role_permissions = RolePermission.objects.filter(role=user.role).select_related("permission")

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "learning_goal": user.learning_goal,
            "first_name": user.first_name,
            "email": user.email,
            "username": user.username,
            "role": user.role.name,
            "last_name": user.last_name,
            "Permissions": [rp.permission.slug for rp in role_permissions],
        }, status=status.HTTP_200_OK)

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

    def delete(self, request, pk):
        """
        DELETE /api/users/<id>/safe_delete/
        """
        result = safe_delete_user(pk)

        if result.startswith("✅"):
            return Response({"message": result}, status=status.HTTP_200_OK)
        else:
            return Response({"error": result}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [HasModelPermission]

    app_label = "accounts"
    model_name = "post"

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
            {"message": "Post deleted successfully"},
            status=status.HTTP_200_OK
        )

# -------------------------------
# ROLE VIEWSET
# -------------------------------
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Role deleted successfully"},
            status=status.HTTP_200_OK
        )  

# -------------------------------
# PERMISSION VIEWSET
# -------------------------------
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Permission deleted successfully"},
            status=status.HTTP_200_OK
        )

# -------------------------------
# ROLE PERMISSION VIEWSET
# -------------------------------
class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "RolesPermission deleted successfully"},
            status=status.HTTP_200_OK
        )

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the profile of the logged-in user"""
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure profile is linked to the logged-in user"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Profile deleted successfully"},
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        Token.objects.filter(user=user).delete()

        recent_log_exists = UserLog.objects.filter(
            user=user,
            action="logout",
            timestamp__gte=timezone.now() - timedelta(seconds=5)
        ).exists()
        if not recent_log_exists:
            UserLog.objects.create(
                user=user,
                action="logout",
                ip_address=get_client_ip(request)
            )

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)