from rest_framework import viewsets, permissions
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Avg

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by("-id")
    serializer_class = AssignmentSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save()
    @action(detail=False, methods=["get"], url_path="total")
    def total_assignment(self, request):
        total = Assignment.objects.count()
        return Response(
            {"total_assignment": total},
            status=status.HTTP_200_OK
        )
    @action(detail=False, methods=["get"], url_path="average-score")
    def average_score(self, request):
        avg_score = Assignment.objects.aggregate(avg=Avg("points"))["avg"] or 0
        percentage = round(avg_score, 2)
        return Response(
            {"average_score": f"{percentage}%"},
            status=status.HTTP_200_OK
        )
    
class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by("-submitted_at")
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save()
