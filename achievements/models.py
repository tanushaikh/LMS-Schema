from django.db import models

class Achievement(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='ach_Achievement_user')
    title = models.CharField(max_length=200)
    description = models.TextField()
    earned_on = models.DateTimeField()
    icon = models.ImageField(upload_to='achievements/')
    slug = models.SlugField(unique=True)

class Certificate(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='ach_Certificate_user')
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    issued_on = models.DateTimeField()
    certificate_file = models.FileField(upload_to='certificates/')
    slug = models.SlugField(unique=True)

class Analytics(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE,related_name='ach_analytics_user')
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    progress_percent = models.FloatField()
    sessions_completed = models.IntegerField()
    last_active = models.DateTimeField()
    slug = models.SlugField(unique=True)
