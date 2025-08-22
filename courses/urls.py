from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, MeetingViewSet,CourseEnrollmentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'meetings', MeetingViewSet, basename='meeting')

router.register(r'enrollments', CourseEnrollmentViewSet, basename='courseenrollment')

urlpatterns = [
    path('', include(router.urls)),
]
