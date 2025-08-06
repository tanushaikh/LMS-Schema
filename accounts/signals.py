from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserLog
from django.utils.timezone import now

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='login', ip_address=get_client_ip(request))

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='logout', ip_address=get_client_ip(request))

@receiver(post_save, sender=User)
def log_register_or_update(sender, instance, created, **kwargs):
    action = 'register' if created else 'update'
    UserLog.objects.create(user=instance, action=action)

@receiver(pre_delete, sender=User)
def log_delete(sender, instance, **kwargs):
    UserLog.objects.create(user=instance, action='delete')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
