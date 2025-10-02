from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet,WeeklyGoalsView

router = DefaultRouter()

router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
    path('weekly-goals/', WeeklyGoalsView.as_view(), name='weekly-goals'),

]
