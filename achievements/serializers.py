from rest_framework import serializers
from .models import Achievement,Certificate,Analytics

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "title", "description","earned_on"]  
        read_only_fields = ['slug']
    
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "user", "course","issued_on","certificate_file"]
        read_only_fields = ['slug']

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = ["id", "user", "course","progress_percent","sessions_completed","last_active "]
        read_only_fields = ['slug']
