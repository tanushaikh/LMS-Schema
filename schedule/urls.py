from rest_framework import routers
from django.urls import path, include
from .views import ScheduleViewSet

router = routers.DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')  # plural "schedules"

urlpatterns = [
    path('', include(router.urls)),
]
