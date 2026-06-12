from .models import Admin, UserApp


def get_user(user_id: int) -> UserApp:
    return UserApp.objects.select_related("user_interface").get(user_id=user_id)


def get_admin(user_id: int) -> Admin:
    return UserApp.objects.select_related("admin_interface").get(user__user_id=user_id)


def get_userapp_with_user(user_id: int) -> UserApp:
    return UserApp.objects.select_related("user").get(user_id=user_id)


def get_userapp_with_admin(user_id: int) -> UserApp:
    return UserApp.objects.select_related("admin").get(user_id=user_id)
