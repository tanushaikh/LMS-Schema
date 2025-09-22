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

        # Determine action
        perm_type = action_permission_map.get(view.action)
        if not perm_type:
            return False

        # Superuser bypass
        if user.is_superuser:
            return True

        # Check user role permission
        return user.has_permission(view.app_label, view.model_name, perm_type)
