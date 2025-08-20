from rest_framework import viewsets
from .models import Achievement, Certificate, Analytics
from .serializers import AchievementSerializer, CertificateSerializer, AnalyticsSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by("-earned_on")
    serializer_class = AchievementSerializer
    permission_classes = []  # 🔓 No auth required


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("-issued_on")
    serializer_class = CertificateSerializer
    permission_classes = []  # 🔓 No auth required


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all().order_by("-last_active")
    serializer_class = AnalyticsSerializer
    permission_classes = []  # 🔓 No auth required
