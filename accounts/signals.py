import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserLog, Post, Profile

logger = logging.getLogger('lmsapp')
User = get_user_model()


def log_action(user, action, instance):
    """Helper to log actions in UserLog + system log"""
    model_name = instance.__class__.__name__
    UserLog.objects.create(
        user=user if isinstance(user, User) else None,
        action=action,
        model_name=model_name
    )
    logger.info(f"{user} - {action} on {model_name} (ID: {instance.pk})")


# -------------------------------
# USER LOGGING
# -------------------------------
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    action = "Created User" if created else "Updated User"
    log_action(instance, action, instance)


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    log_action(instance, "Deleted User", instance)


# -------------------------------
# POST LOGGING
# -------------------------------
@receiver(post_save, sender=Post)
def log_post_save(sender, instance, created, **kwargs):
    action = "Created Post" if created else "Updated Post"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Post)
def log_post_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Post", instance)


# -------------------------------
# PROFILE LOGGING
# -------------------------------
@receiver(post_save, sender=Profile)
def log_profile_save(sender, instance, created, **kwargs):
    action = "Created Profile" if created else "Updated Profile"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Profile)
def log_profile_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Profile", instance)
