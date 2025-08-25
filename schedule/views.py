from rest_framework import viewsets
from .models import Schedule
from .serializers import ScheduleSerializer

# Create your views here.
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer