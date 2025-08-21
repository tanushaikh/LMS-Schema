from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from accounts.serializers import RegisterSerializer, LoginSerializer,PostSerializer,RolePermissionSerializer,PermissionSerializer,RoleSerializer
from accounts.models import UserLog, User,Post,RolePermission,Role,Permission
from datetime import timedelta
from django.utils import timezone
import logging
from rest_framework import viewsets, permissions,status
from rest_framework.permissions import IsAuthenticated
from lms.models import *
logger = logging.getLogger('lmsapp')
User = get_user_model()

from django.db import transaction, DatabaseError

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


class LoginView(APIView):
    def post(self, request):
        logger.info("Login API called")

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"Login successful for user: {username}")

            recent_log_exists = UserLog.objects.filter(
                user=user,
                action='login',
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            if not recent_log_exists:
                UserLog.objects.create(user=user, action='login', ip_address=get_client_ip(request))

            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)

        logger.warning(f"Invalid login attempt for username: {username}")
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# class UserDetailView(APIView):

#     def get(self, request, pk):
#         logger.info(f"{request.user.email} fetching user id={pk}")
#         user_obj = get_object_or_404(User, pk=pk)
#         serializer = RegisterSerializer(user_obj)
#         return Response({'data': serializer.data})

class UserDetailView(APIView):
    """
    Update user details by ID.
    """

    def put(self, request, pk):
        # Fetch the user object by ID
        user_obj = get_object_or_404(User, pk=pk)

        # Update the user with the request data
        serializer = RegisterSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Log the update action
            recent_log_exists = UserLog.objects.filter(
                user=request.user if request.user.is_authenticated else None,
                action='update_user',
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            if not recent_log_exists and request.user.is_authenticated:
                UserLog.objects.create(
                    user=request.user,
                    action='update_user',
                    ip_address=get_client_ip(request)
                )

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        """
        Delete user by ID with comprehensive foreign key handling.
        """
        from django.db import transaction, connection
        from django.apps import apps
        
        # Fetch the user object by ID
        user_obj = get_object_or_404(User, id=id)
        user_identifier = user_obj.email if user_obj.email else user_obj.username
        
        try:
            with transaction.atomic():
                if connection.vendor == 'sqlite':
                    with connection.cursor() as cursor:
                        cursor.execute('PRAGMA foreign_keys = OFF')
                
                user_id = user_obj.id
                
                cleanup_models = [
                    ('accounts', 'UserLog', 'user_id'),
                    ('accounts', 'Post', 'user_id'),
                    ('accounts', 'Profile', 'user_id'),                    
                    ('lms', 'Profile', 'user_id'),
                    ('lms', 'Course', 'created_by_id'),
                    ('lms', 'Meeting', 'host_id'),
                    ('lms', 'Assignment', 'created_by_id'),
                    ('lms', 'AssignmentSubmission', 'user_id'),
                    ('lms', 'AITutorInteraction', 'user_id'),
                    ('lms', 'Achievement', 'user_id'),
                    ('lms', 'Certificate', 'user_id'),
                    ('lms', 'Analytics', 'user_id'),
                    ('lms', 'Notification', 'user_id'),
                    ('lms', 'Feedback', 'user_id'),
                    ('lms', 'CourseEnrollment', 'user_id'),
                    ('lms', 'Bookmark', 'user_id'),
                    ('lms', 'Discussion', 'user_id'),
                ]
                
                with connection.cursor() as cursor:
                    for app_name, model_name, field_name in cleanup_models:
                        try:
                            model = apps.get_model(app_name, model_name)
                            table_name = model._meta.db_table
                            
                            cursor.execute(f'DELETE FROM {table_name} WHERE {field_name} = %s', [user_id])
                            
                        except (LookupError, Exception) as e:
                            print(f"Skipping {app_name}.{model_name}: {e}")
                            continue
                    
                    cursor.execute('DELETE FROM accounts_user WHERE id = %s', [user_id])
                
                if connection.vendor == 'sqlite':
                    with connection.cursor() as cursor:
                        cursor.execute('PRAGMA foreign_keys = ON')
            
            if request.user.is_authenticated and request.user.id != user_id:
                try:
                    recent_log_exists = UserLog.objects.filter(
                        user=request.user,
                        action='delete_user',
                        timestamp__gte=timezone.now() - timedelta(seconds=5)
                    ).exists()
                    
                    if not recent_log_exists:
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
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            return Response(
                {'error': f'Failed to delete user: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


    def soft_delete(self, request, id):
        """
        Alternative: Soft delete user by setting is_active to False
        """
        user_obj = get_object_or_404(User, id=id)
        
        user_identifier = user_obj.email if user_obj.email else user_obj.username
        
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