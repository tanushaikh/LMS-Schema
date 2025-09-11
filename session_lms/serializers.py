from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()  # backend generate karega
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # frontend se mat bhejna

    class Meta:
        model = Session
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": False, "allow_null": True},
            "slug": {"read_only": True},
        }
