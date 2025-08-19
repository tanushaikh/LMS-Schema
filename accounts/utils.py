# accounts/utils.py
def has_permission(user, app_model, action):
    if not user.role:
        return False
    return user.role.permissions.filter(
        permission__app_model=app_model,
        permission__action=action
    ).exists()
