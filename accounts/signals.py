import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserLog, Post, Profile
from courses.models import *

from assignments.models import *
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


# -------------------------------
# ASSIGNMENT LOGGING
# -------------------------------
@receiver(post_save, sender=Assignment)
def log_assignment_save(sender, instance, created, **kwargs):
    action = "Created Assignment" if created else "Updated Assignment"
    log_action(instance.created_by, action, instance)


@receiver(post_delete, sender=Assignment)
def log_assignment_delete(sender, instance, **kwargs):
    log_action(instance.created_by, "Deleted Assignment", instance)


# -------------------------------
# ASSIGNMENT SUBMISSION LOGGING
# -------------------------------
@receiver(post_save, sender=AssignmentSubmission)
def log_submission_save(sender, instance, created, **kwargs):
    action = "Created Submission" if created else "Updated Submission"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=AssignmentSubmission)
def log_submission_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Submission", instance)
    

# -------------------------------
# COURSES 
# -------------------------------
@receiver(post_save, sender=Course)
def log_course_save(sender, instance, created, **kwargs):
    action = "Created Course" if created else "Updated Course"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted course", instance)
    
    
    
# -------------------------------
# Meeting 
# -------------------------------
@receiver(post_save, sender=Course)
def log_course_save(sender, instance, created, **kwargs):
    action = "Created Course" if created else "Updated Course"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted course", instance)
    

# -------------------------------
# Session
# -------------------------------
@receiver(post_save, sender=Session)
def log_session_save(sender, instance, created, **kwargs):
    action = "Created Session" if created else "Updated Session"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Session)
def log_session_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Session", instance)
    
    
# -------------------------------
# CourseEnrollment
# -------------------------------
@receiver(post_save, sender=CourseEnrollment)
def log_course_enrollment_save(sender, instance, created, **kwargs):
    action = "Created CourseEnrollment" if created else "Updated CourseEnrollment"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=CourseEnrollment)
def log_course_enrollment_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted CourseEnrollment", instance)
    
    
    