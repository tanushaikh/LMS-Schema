from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from accounts.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from accounts.models import UserLog  # Import your log model
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger('lmsapp') 


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Check if a recent register log exists (within 5 seconds)
            recent_log_exists = UserLog.objects.filter(user=user,action='register',timestamp__gte=timezone.now() - timedelta(seconds=5)).exists()
            if recent_log_exists:
                UserLog.objects.create(user=user,action='register',ip_address=get_client_ip(request))

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
            return Response({"message": "Login successful"})
        
        logger.warning(f"Invalid login attempt for username: {username}")
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ProfileView(APIView):
    def post(self, request):
        logger.info("Login API called")

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"Login successful for user: {username}")
            return Response({"message": "Login successful"})
        
        logger.warning(f"Invalid login attempt for username: {username}")
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
