from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule
from .serializers import ScheduleSerializer
from accounts.models import User
from accounts.permissions import HasModelPermission

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [HasModelPermission]

    app_label = "schedule"
    model_name = "schedule"

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
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            default_user = User.objects.first()  # fallback user
            serializer.save(user=default_user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Schedule deleted successfully"},
            status=status.HTTP_200_OK
        )
