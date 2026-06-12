from importlib import reload

from django.db import models

from dana.common.models import BaseModel


class UserApp(BaseModel):
    """
    hint :
        that user service is that various layer that manages user data
        Authentication Service with JWT
        this model just that refreence to This App service

        that Pyload from Auth Service is {
        {

            "user_id": user.id,
            "username": user.username,
            "user_email": user.email,
            "user_role": user.role,
            "token": token,
        }
    """

    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    user_id = models.BigIntegerField(unique=True, db_index=True)

    username = models.CharField(max_length=30, unique=True, db_index=True)

    user_email = models.EmailField(db_index=True)

    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER
    )

    last_synced_at = models.DateTimeField(auto_now=True)

    token_hash = models.CharField(max_length=64, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["username"]),
        ]

    def __str__(self) -> str:
        return f"{self.username} ({self.user_id})"


class Admin(BaseModel):
    user = models.OneToOneField(
        UserApp, on_delete=models.CASCADE, related_name="admin_interface"
    )

    def save(self, *args, **kwargs):
        if (
            self.user.user_interface
        ):  # TODO use django signall for handel this opreation
            raise ValueError("User already has an admin interface")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.user.user_id})"


class User(BaseModel):
    user = models.OneToOneField(
        UserApp, on_delete=models.CASCADE, related_name="user_interface"
    )

    def save(self, *args, **kwargs):
        if (
            self.user.admin_interface
        ):  # TODO use django signall for handel this opreation
            raise ValueError("User already has an admin interface")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.user.user_id})"
