from rest_framework import viewsets
from .models import Achievement, Certificate, Analytics
from .serializers import AchievementSerializer, CertificateSerializer, AnalyticsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from accounts.permissions import HasModelPermission
from django.utils.text import slugify

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by("-earned_on")
    serializer_class = AchievementSerializer
    permission_classes = []  # 🔓 No auth required
    @action(detail=False, methods=["get"], url_path="total")
    def total_achievement(self, request):
        total = Achievement.objects.count()
        return Response(
            {"total_achievement": total},
            status=status.HTTP_200_OK
        )
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Achievement deleted successfully"},
            status=status.HTTP_200_OK
        )

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("-issued_on")
    serializer_class = CertificateSerializer
    permission_classes = [HasModelPermission]

    app_label = "achievements"
    model_name = "certificate"
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


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all().order_by("-last_active")
    serializer_class = AnalyticsSerializer
    permission_classes = []  # 🔓 No auth required
