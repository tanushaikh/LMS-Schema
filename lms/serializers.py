from rest_framework import serializers
from .models import AITutorInteraction, ContactUs, LiveClass, Notification, Feedback, Bookmark, Discussion,Blog, OnDemandClass, UpcomingEvent

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

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

from rest_framework import serializers
from .models import FAQCategory, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']


class FAQCategorySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = FAQCategory
        fields = ['id', 'title', 'icon', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        category = FAQCategory.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(category=category, **question_data)
        return category

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        instance.title = validated_data.get('title', instance.title)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()

        instance.questions.all().delete()  # clear old questions
        for question_data in questions_data:
            Question.objects.create(category=instance, **question_data)
        return instance

class LiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = '__all__'


class OnDemandClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnDemandClass
        fields = '__all__'


class UpcomingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingEvent
        fields = '__all__'
