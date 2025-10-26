from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AITutorInteractionViewSet,
    BlogViewSet,
    ContactUsViewSet,
    NotificationViewSet,
    FeedbackViewSet,
    BookmarkViewSet,
    DiscussionViewSet,
    FAQCategoryViewSet,
)

router = DefaultRouter()
router.register(r'ai-interactions', AITutorInteractionViewSet, basename='ai-interaction')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'discussions', DiscussionViewSet, basename='discussion')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'contact', ContactUsViewSet, basename='contactus')
router.register(r'faq', FAQCategoryViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]
