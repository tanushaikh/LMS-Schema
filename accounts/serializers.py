from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile,Post,Role,RolePermission,Permission,UserLog
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    raw_password = None
    raw_confirm_password = None

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 'confirm_password',
            'user_type', 'first_name', 'last_name', 'learning_goal'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate_first_name(self, value):
        """Ensure first_name is unique"""
        if User.objects.filter(first_name=value).exists():
            raise serializers.ValidationError("This first name is already taken.")
        return value

    def validate_last_name(self, value):
        """Ensure last_name is unique"""
        if User.objects.filter(last_name=value).exists():
            raise serializers.ValidationError("This last name is already taken.")
        return value

    def validate_learning_goal(self, value):
        """Ensure learning_goal is unique"""
        if User.objects.filter(learning_goal=value).exists():
            raise serializers.ValidationError("This learning goal is already taken.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        self.raw_password = validated_data['password']
        self.raw_confirm_password = validated_data['confirm_password']

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['confirm_password'] = make_password(validated_data['confirm_password'])

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if password:
            self.raw_password = password
            instance.password = make_password(password)

        if confirm_password:
            self.raw_confirm_password = confirm_password
            instance.confirm_password = make_password(confirm_password)

        for attr, value in validated_data.items():
            if attr not in ['password', 'confirm_password']:
                setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['password'] = self.raw_password if self.raw_password else "******"
        rep['confirm_password'] = self.raw_confirm_password if self.raw_confirm_password else "******"
        return rep

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
        


# -------------------------------
# PROFILE SERIALIZER
# -------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "full_name", "age", "gender", "bio",
                  "profile_picture", "mobile", "country", "slug"]


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

        fields = ['id', 'app_label', 'model_name', 'permission_type', 'slug']


# -------------------------------
# ROLE PERMISSION SERIALIZER
# -------------------------------
class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), write_only=True, source="role"
    )
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), write_only=True, source="permission"
    )

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'slug', 'role_id', 'permission_id']

# -------------------------------
#       PROFILE SERIALIZER
# -------------------------------

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# -------------------------------
#       POST SERIALIZER
# -------------------------------



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'