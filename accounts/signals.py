# from django.contrib.auth.signals import user_logged_in, user_logged_out
# from django.db.models.signals import post_save, pre_delete
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import UserLog
# from django.utils.timezone import now
# import logging
# @receiver(user_logged_in)
# def log_login(sender, request, user, **kwargs):
#     UserLog.objects.create(user=user, action='login', ip_address=get_client_ip(request))

# @receiver(user_logged_out)
# def log_logout(sender, request, user, **kwargs):
#     UserLog.objects.create(user=user, action='logout', ip_address=get_client_ip(request))

# @receiver(post_save, sender=User)
# def log_register_or_update(sender, instance, created, **kwargs):
#     action = 'register' if created else 'update'
#     UserLog.objects.create(user=instance, action=action)

# @receiver(pre_delete, sender=User)
# def log_delete(sender, instance, **kwargs):
#     UserLog.objects.create(user=instance, action='delete')

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
# from .models import Course  # Example model

logger = logging.getLogger('lmsapp')

User = get_user_model()

# Log CREATE and UPDATE
@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    # Avoid logging for irrelevant system models
    if sender.__name__ in ['Session', 'LogEntry', 'ContentType', 'Permission']:
        return

    if created:
        logger.info(f"Created new {sender.__name__} with ID {instance.pk}")
    else:
        logger.info(f"Updated {sender.__name__} with ID {instance.pk}")

# Log DELETE
@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender.__name__ in ['Session', 'LogEntry', 'ContentType', 'Permission']:
        return

    logger.warning(f"Deleted {sender.__name__} with ID {instance.pk}")

