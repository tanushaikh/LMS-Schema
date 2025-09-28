from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, AssignmentSubmissionViewSet, AssignmentTotalAPIView, AssignmentAverageScoreAPIView

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename="assignments")
router.register(r'submissions', AssignmentSubmissionViewSet, basename="submissions")

urlpatterns = [
    path("", include(router.urls)),
    path("total/", AssignmentTotalAPIView.as_view(), name="assignment-total"),
    path("average-score/", AssignmentAverageScoreAPIView.as_view(), name="assignment-average-score"),

]
