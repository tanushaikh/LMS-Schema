from django.shortcuts import render
from .models import Session
from rest_framework import viewsets
from .serializers import SessionSerializer
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
