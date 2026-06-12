from django.db import transaction

from .models import Admin, User, UserApp


@transaction.atomic
def create_user(*, user_id: int) -> User:
    user_app = UserApp.objects.select_for_update().get(user_id=user_id)

    user, _ = User.objects.get_or_create(user=user_app)
    return user


@transaction.atomic
def create_admin(*, user_id: int) -> Admin:
    user_app = UserApp.objects.select_for_update().get(user_id=user_id)
    admin, _ = Admin.objects.get_or_create(user=user_app)
    return admin
