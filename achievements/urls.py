from django.urls import path
from .views import *

urlpatterns = [
    # Achievement
    path('achievement/', AchievementListCreateView.as_view(), name='achievement-list-create'),
    path('achievement/<int:pk>/', AchievementDetailView.as_view(), name='achievement-detail'),

    # Certificate
    path('certificate/', CertificateListCreateView.as_view(), name='certificate-list-create'),
    path('certificate/<int:pk>/', CertificateDetailView.as_view(), name='certificate-detail'),

    # Analytics
    path('analytics/', AnalyticsListCreateView.as_view(), name='analytics-list-create'),
    path('analytics/<int:pk>/', AnalyticsDetailView.as_view(), name='analytics-detail'),
]
