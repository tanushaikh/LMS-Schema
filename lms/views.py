from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import AITutorInteraction, Notification, Feedback, Bookmark, Discussion
from .serializers import (
    AITutorInteractionSerializer,
    NotificationSerializer,
    FeedbackSerializer,
    BookmarkSerializer,
    DiscussionSerializer
)

class AITutorInteractionViewSet(viewsets.ModelViewSet):
    queryset = AITutorInteraction.objects.all()
    serializer_class = AITutorInteractionSerializer
    permission_classes = [AllowAny]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [AllowAny]


class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [AllowAny]
