from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Avg
from accounts.permissions import HasModelPermission

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by("-id")
    serializer_class = AssignmentSerializer
    permission_classes = [HasModelPermission]

    app_label = "assignments"
    model_name = "assignment"

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
        serializer.save()

        # 👇 delete response customize
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Assignment deleted successfully"},
            status=status.HTTP_200_OK
        )
    

class AssignmentTotalAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "assignments"
    model_name = "assignment"
    permission_type = "view" 

    def get(self, request, *args, **kwargs):
        total = Assignment.objects.count()
        return Response(
            {"total_assignment": total},
            status=status.HTTP_200_OK
        )


class AssignmentAverageScoreAPIView(APIView):
    permission_classes = [HasModelPermission]
    app_label = "assignments"
    model_name = "assignment"
    permission_type = "view"

    def get(self, request, *args, **kwargs):
        avg_score = Assignment.objects.aggregate(avg=Avg("points"))["avg"] or 0
        percentage = round(avg_score, 2)
        return Response(
            {"average_score": f"{percentage}%"},
            status=status.HTTP_200_OK
        )
class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by("-submitted_at")
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [HasModelPermission]

    app_label = "assignments"
    model_name = "assignmentsubmission"

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
        serializer.save()
        
    # 👇 delete response customize
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Submission deleted successfully"},
            status=status.HTTP_200_OK
        )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Submission created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
