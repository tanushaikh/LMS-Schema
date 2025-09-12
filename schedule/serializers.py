from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False, "allow_null": True},  # user not required
        }
