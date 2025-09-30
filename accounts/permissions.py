from rest_framework import permissions


class HasModelPermission(permissions.BasePermission):
    """
    Dynamic permission check based on user role and action.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        action_permission_map = {
            "create": "add",
            "list": "view",
            "retrieve": "view",
            "update": "edit",
            "partial_update": "edit",
            "destroy": "delete",
        }

        if hasattr(view, "action"):
            perm_type = action_permission_map.get(view.action)
        else:
            perm_type = getattr(view, "permission_type", None)

        if not perm_type:
            return False

        if user.is_superuser:
            return True

        return user.has_permission(view.app_label, view.model_name, perm_type)


# 👇 ye tumhare analytics ke liye specific permission hai
class WeeklyAnalyticsPermission(permissions.BasePermission):
    """
    Check if user has 'view' permission for course enrollment and assignment submission
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # yaha dono permission check honi chahiye
        return (
            user.has_permission("courses", "courseenrollment", "view")
            and user.has_permission("assignments", "assignmentsubmission", "view")
        )
