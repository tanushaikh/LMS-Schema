from django.contrib.admin.models import LogEntry
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db import transaction, connection
from .models import RolePermission
def has_permission(user, app_model, action):
    if not user.role:
        return False
    return user.role.permissions.filter(
        permission__app_model=app_model,
        permission__action=action
    ).exists()



User = get_user_model()

def safe_delete_user(user_id: int) -> str:
    """
    Safely delete a user:
      - Cleans tokens
      - Nullifies log entries
      - Sets all other FKs to NULL (if possible)
      - Force deletes user row to avoid CASCADE issues
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"❌ User {user_id} does not exist."

    with transaction.atomic():
        Token.objects.filter(user=user).delete()

        LogEntry.objects.filter(user=user).update(user=None)

        for rel in user._meta.related_objects:
            rel_manager = getattr(user, rel.get_accessor_name(), None)
            if rel_manager is None:
                continue

            if rel.field.null:
                rel_manager.update(**{rel.field.name: None})
            else:
                rel_manager.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM {table} WHERE id = %s".format(
                table=User._meta.db_table
            ), [user.id])

    return f"✅ User {user_id} deleted safely."


def user_has_permission(user, app_label, model_name, permission_type):
    if user.is_superuser or user.is_staff:
        return True
    if not user.role:
        return False
    return RolePermission.objects.filter(
        role=user.role,
        permission__app_label=app_label,
        permission__model_name=model_name,
        permission__permission_type=permission_type,
    ).exists()

# accounts/utils.py
from assignments.models import AssignmentSubmission
from django.utils import timezone
from datetime import timedelta

def get_weekly_goals(user):
    """
    Returns number of assignments completed in the last 7 days by the user
    """
    today = timezone.now().date()
    week_ago = today - timedelta(days=6)

    completed = AssignmentSubmission.objects.filter(
        user=user,
        submitted_on__date__range=[week_ago, today],
        status="completed"
    ).count()

    return {
        "weekly_completed": completed,
        "goal": 5,  # yaha tum apna logic daal sakti ho (e.g., weekly goal = 5 assignments)
        "status": "achieved" if completed >= 5 else "in-progress"
    }
