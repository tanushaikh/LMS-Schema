from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, CertificateViewSet, AnalyticsViewSet,WeeklyAnalyticsView

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet, basename="achievements")
router.register(r'certificates', CertificateViewSet, basename="certificates")
router.register(r'analytics', AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path('', include(router.urls)),
    path("weekly/", WeeklyAnalyticsView.as_view(), name="weekly-analytics"),

]
