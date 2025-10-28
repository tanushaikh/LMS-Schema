from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.permissions import HasModelPermission
from .models import AITutorInteraction, Blog, ContactUs, LiveClass, Notification, Feedback, Bookmark, Discussion, OnDemandClass, UpcomingEvent,FAQCategory
from .serializers import (
    AITutorInteractionSerializer,
    BlogSerializer,
    ContactUsSerializer,
    LiveClassSerializer,
    NotificationSerializer,
    FeedbackSerializer,
    BookmarkSerializer,
    DiscussionSerializer,
    OnDemandClassSerializer,
    UpcomingEventSerializer,
    FAQCategorySerializer,
)

class AITutorInteractionViewSet(viewsets.ModelViewSet):
    queryset = AITutorInteraction.objects.all()
    serializer_class = AITutorInteractionSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "aitutorinteraction"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "AITutorInteraction deleted successfully"},
            status=status.HTTP_200_OK
        )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "notification"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "notification deleted successfully"},
            status=status.HTTP_200_OK
        )


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "feedback"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "feedback deleted successfully"},
            status=status.HTTP_200_OK
        )


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "bookmark"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "bookmark deleted successfully"},
            status=status.HTTP_200_OK
        )


class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "discussion"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "discussion deleted successfully"},
            status=status.HTTP_200_OK
        )

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "blog"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Blog deleted successfully"},
            status=status.HTTP_200_OK
        )

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [HasModelPermission]

    app_label = "lms"
    model_name = "contactus"

    def get_permissions(self):
        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }
        self.permission_type = action_permission_map.get(self.action, None)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Contact Us deleted successfully"},
            status=status.HTTP_200_OK
        )

class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer


class LiveClassViewSet(viewsets.ModelViewSet):
    queryset = LiveClass.objects.all()
    serializer_class = LiveClassSerializer


class OnDemandClassViewSet(viewsets.ModelViewSet):
    queryset = OnDemandClass.objects.all()
    serializer_class = OnDemandClassSerializer


class UpcomingEventViewSet(viewsets.ModelViewSet):
    queryset = UpcomingEvent.objects.all()
    serializer_class = UpcomingEventSerializer
