from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile,Post
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            is_active=False
        )
        return user
    def update(self, instance, validated_data):
            password = validated_data.pop('password', None)  # remove password if exists
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if password:
                instance.set_password(password)  # hash password
            instance.save()
            return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
    
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")  # show email instead of ID

    class Meta:
        model = Post
        fields = ["id", "user", "title", "content", "created_at", "updated_at", "slug"]
        read_only_fields = ["id", "user", "created_at", "updated_at", "slug"]