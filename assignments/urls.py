from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, AssignmentSubmissionViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename="assignments")
router.register(r'submissions', AssignmentSubmissionViewSet, basename="submissions")

urlpatterns = [
    path("", include(router.urls)),
]
