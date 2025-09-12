import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserLog, Post, Profile
from courses.models import *
from achievements.models import *
from lms.models import *
from schedule.models import Schedule
from session_lms.models import Session
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
    log_action(instance.created_by, action, instance)


@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    log_action(instance.created_by, "Deleted course", instance)
    
    
# -------------------------------
# Meeting 
# -------------------------------
@receiver(post_save, sender=Meeting)
def log_meeting_save(sender, instance, created, **kwargs):
    action = "Created Meeting" if created else "Updated Meeting"
    if instance.host:  # check host exists
        log_action(instance.host, action, instance)

@receiver(post_delete, sender=Meeting)
def log_meeting_delete(sender, instance, **kwargs):
    if instance.host:
        log_action(instance.host, "Deleted Meeting", instance)

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
    
    
# -------------------------------
#Achievement
# -------------------------------
@receiver(post_save, sender=Achievement)
def log_achievement_save(sender, instance, created, **kwargs):
    action = "Created Achievement" if created else "Updated Achievement"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Achievement)
def log_achievement_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Achievement", instance)
    

# -------------------------------
#Certificate
# -------------------------------
@receiver(post_save, sender=Certificate)
def log_certificate_save(sender, instance, created, **kwargs):
    action = "Created Certificate" if created else "Updated Certificate"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Certificate)
def log_certificate_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Certificate", instance)
# -------------------------------
#Analytics
# -------------------------------
@receiver(post_save, sender=Analytics)
def log_analytics_save(sender, instance, created, **kwargs):
    action = "Created Analytics" if created else "Updated Analytics"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=Analytics)
def log_analytics_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted Analytics", instance)  
    

# -------------------------------
#AITutorInteraction/lms
# -------------------------------
@receiver(post_save, sender=AITutorInteraction)
def log_aITutorinteraction_save(sender, instance, created, **kwargs):
    action = "Created AITutorInteraction" if created else "Updated AITutorInteraction"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender=AITutorInteraction)
def log_AITutorinteraction_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted AITutorInteraction", instance)  
    
    
# -------------------------------
# Notification/lms
# -------------------------------
@receiver(post_save, sender= Notification)
def log_notification_save(sender, instance, created, **kwargs):
    action = "Created  Notification" if created else "Updated  Notification"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender= Notification)
def log_notification_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted  Notification", instance) 
    
# -------------------------------
# Feedback/lms
# -------------------------------
@receiver(post_save, sender= Feedback)
def log_feedback_save(sender, instance, created, **kwargs):
    action = "Created  Feedback" if created else "Updated  Feedback"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender= Feedback)
def log_feedback_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted  Feedback", instance) 
    
# -------------------------------
# Bookmark/lms
# -------------------------------
@receiver(post_save, sender= Bookmark)
def log_bookmark_save(sender, instance, created, **kwargs):
    action = "Created  Bookmark" if created else "Updated  Bookmark"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender= Bookmark)
def log_bookmark_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted  Bookmark", instance)     
    
# -------------------------------
# Discussion/lms
# -------------------------------
@receiver(post_save, sender= Discussion)
def log_discussion_save(sender, instance, created, **kwargs):
    action = "Created  Discussion" if created else "Updated  Discussion"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender= Discussion)
def log_discussion_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted  Discussion", instance) 
    
        
    # -------------------------------
# schedule/lmsschedule
# -------------------------------
@receiver(post_save, sender= Schedule)
def log_schedule_save(sender, instance, created, **kwargs):
    action = "Created  schedule" if created else "Updated  schedule"
    log_action(instance.user, action, instance)


@receiver(post_delete, sender= Schedule)
def log_schedule_delete(sender, instance, **kwargs):
    log_action(instance.user, "Deleted  schedule", instance) 
    