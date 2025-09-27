from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Post, Role, RolePermission, Permission,Profile
from django.contrib.auth import authenticate


# -------------------------------
# REGISTER SERIALIZER
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 'confirm_password',
            'first_name', 'last_name', 'learning_goal', 'role_id'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role_id')
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = role

        user = User.objects.create(**validated_data)

        Profile.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}".strip() or user.username
        )

        return user


# -------------------------------
# POST SERIALIZER
# -------------------------------
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Post
        fields = ["id", "user", "title", "content", "created_at", "updated_at", "slug"]
# -------------------------------
# LOGIN SERIALIZER
# -------------------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")



# -------------------------------
# ROLE SERIALIZER
# -------------------------------
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description", "slug"]


# -------------------------------
# PERMISSION SERIALIZER
# -------------------------------
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "app_label", "model_name", "permission_type", "slug"]


# -------------------------------
# ROLE PERMISSION SERIALIZER
# -------------------------------
class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, source="role")
    permission_id = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), write_only=True, source="permission")

    class Meta:
        model = RolePermission
        fields = ["id", "role", "permission", "slug", "role_id", "permission_id"]

# -------------------------------
# POST SERIALIZER
# -------------------------------
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")  # show email instead of ID

    class Meta:
        model = Post
        fields = ["id", "user", "title", "content", "created_at", "updated_at", "slug"]
        read_only_fields = ["id", "user", "created_at", "updated_at", "slug"]


# -------------------------------
# PROFILE SERIALIZER
# -------------------------------
# serializers.py

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "user", "full_name", "age", "gender", "bio",
                  "profile_picture", "mobile", "country", "slug"]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "learning_goal": obj.user.learning_goal,
            "role": obj.user.role.name if obj.user.role else None,
        }
