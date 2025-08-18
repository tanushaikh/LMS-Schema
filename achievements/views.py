from django.shortcuts import get_object_or_404
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import UserLog
from accounts.views import get_client_ip
from .models import Achievement, Certificate, Analytics
from .serializers import AchievementSerializer, CertificateSerializer, AnalyticsSerializer

# ---------------------------
# ACHIEVEMENT CRUD
# ---------------------------
class AchievementListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(achievements, many=True)

        # Logging
        # Log action
        if request.user.is_authenticated:
            recent_log_exists = UserLog.objects.filter(
                user=request.user,
                action=f"get Achievement",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()

            if not recent_log_exists:
                UserLog.objects.create(
                    user=request.user,
                    action=f"get Achievement",
                    ip_address=get_client_ip(request)
                )
        else:
            # Log as anonymous user
            recent_log_exists = UserLog.objects.filter(
                user=None,
                action=f"anonymous get Achievement",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
            ).exists()

            if not recent_log_exists:
                UserLog.objects.create(
                    user=None,
                    action=f"anonymous get Achievement",
                    ip_address=get_client_ip(request)
                )
        return Response(serializer.data)

    def post(self, request):
        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            # Log action
            if request.user.is_authenticated:
                recent_log_exists = UserLog.objects.filter(
                user=request.user,
                action=f"create Achievement",
                timestamp__gte=timezone.now() - timedelta(seconds=5)
                ).exists()

                if not recent_log_exists:
                    UserLog.objects.create(
                    user=request.user,
                    action=f"create Achievement",
                    ip_address=get_client_ip(request)
                )
                else:
                    # Log as anonymous user
                    recent_log_exists = UserLog.objects.filter(
                    user=None,
                    action=f"anonymous create Achievement",
                    timestamp__gte=timezone.now() - timedelta(seconds=5)
                    ).exists()

                    if not recent_log_exists:
                        UserLog.objects.create(
                            user=None,
                            action=f"anonymous createAchievement",
                            ip_address=get_client_ip(request)
                        )
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class AchievementDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        achievement = get_object_or_404(Achievement, pk=pk)
        serializer = AchievementSerializer(achievement)
        self.log_action(request, f"get achievement {pk}")
        return Response(serializer.data)

    def put(self, request, pk):
        achievement = get_object_or_404(Achievement, pk=pk)
        serializer = AchievementSerializer(achievement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.log_action(request, f"update achievement {pk}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        achievement = get_object_or_404(Achievement, pk=pk)
        achievement.delete()
        self.log_action(request, f"delete achievement {pk}")
        return Response({"message": "Achievement deleted"}, status=status.HTTP_204_NO_CONTENT)

    
# ---------------------------
# CERTIFICATE CRUD
# ---------------------------
class CertificateListCreateView(AchievementListCreateView):
    def get(self, request):
        certificates = Certificate.objects.all()
        serializer = CertificateSerializer(certificates, many=True)
        self.log_action(request, "get all certificate")
        return Response(serializer.data)

    def post(self, request):
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            self.log_action(request, "certificate create")
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateDetailView(AchievementDetailView):
    def get(self, request, pk):
        certificate = get_object_or_404(Certificate, pk=pk)
        serializer = CertificateSerializer(certificate)
        self.log_action(request, f"get certificate {pk}")
        return Response(serializer.data)

    def put(self, request, pk):
        certificate = get_object_or_404(Certificate, pk=pk)
        serializer = CertificateSerializer(certificate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.log_action(request, f"update certificate {pk}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        certificate = get_object_or_404(Certificate, pk=pk)
        certificate.delete()
        self.log_action(request, f"delete certificate {pk}")
        return Response({"message": "Certificate deleted"}, status=status.HTTP_204_NO_CONTENT)

# ---------------------------
# ANALYTICS CRUD
# ---------------------------
class AnalyticsListCreateView(AchievementListCreateView):
    def get(self, request):
        analytics = Analytics.objects.all()
        serializer = AnalyticsSerializer(analytics, many=True)
        self.log_action(request, "get all analytics")
        return Response(serializer.data)

    def post(self, request):
        serializer = AnalyticsSerializer(data=request.data)
        if serializer.is_valid():
            self.log_action(request, "analytics create")
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsDetailView(AchievementDetailView):
    def get(self, request, pk):
        analytics = get_object_or_404(Analytics, pk=pk)
        serializer = AnalyticsSerializer(analytics)
        self.log_action(request, f"get analytics {pk}")
        return Response(serializer.data)

    def put(self, request, pk):
        analytics = get_object_or_404(Analytics, pk=pk)
        serializer = AnalyticsSerializer(analytics, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.log_action(request, f"update analytics {pk}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        analytics = get_object_or_404(Analytics, pk=pk)
        analytics.delete()
        self.log_action(request, f"delete analytics {pk}")
        return Response({"message": "Analytics deleted"}, status=status.HTTP_204_NO_CONTENT)
