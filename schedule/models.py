from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Schedule(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    reminder = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reminder_time = models.DateTimeField()
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    participants = models.IntegerField()
    color = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    

