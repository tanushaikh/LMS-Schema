from rest_framework import serializers
from .models import AITutorInteraction, Notification, Feedback, Bookmark, Discussion

class AITutorInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AITutorInteraction
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'
