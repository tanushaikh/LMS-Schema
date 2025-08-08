from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView,
    MeetingListCreateView, MeetingDetailView,
    SessionListCreateView, SessionDetailView,
    CourseEnrollmentListCreateView, CourseEnrollmentDetailView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),

    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),

    path('enrollments/', CourseEnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', CourseEnrollmentDetailView.as_view(), name='enrollment-detail'),
]
