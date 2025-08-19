from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from accounts.serializers import RegisterSerializer, LoginSerializer,PostSerializer
from accounts.models import UserLog, User,Post
from datetime import timedelta
from django.utils import timezone
import logging
from rest_framework import viewsets, permissions,status

logger = logging.getLogger('lmsapp')


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


class UserDetailView(APIView):
    def get(self, request, pk):
        logger.info(f"{request.user.email} fetching user id={pk}")
        user_obj = get_object_or_404(User, pk=pk)
        serializer = RegisterSerializer(user_obj)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        logger.info(f"{request.user.email} updating user id={pk}")
        user_obj = get_object_or_404(User, pk=pk)
        serializer = RegisterSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            recent_log_exists = UserLog.objects.filter(
                user=request.user, action='update_user',
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()
            if not recent_log_exists:
                UserLog.objects.create(user=request.user, action='update_user', ip_address=get_client_ip(request))

            return Response({'data': serializer.data})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"{request.user.email} deleting user id={pk}")
        user_obj = get_object_or_404(User, pk=pk)
        user_obj.delete()

        recent_log_exists = UserLog.objects.filter(
            user=request.user, action='delete_user',
            timestamp__gte=timezone.now() - timedelta(seconds=5)
        ).exists()
        if not recent_log_exists:
            UserLog.objects.create(user=request.user, action='delete_user', ip_address=get_client_ip(request))

        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)