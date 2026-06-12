from django.urls import path

from .routers import (
    CreateAdminApiView,
    CreateUserApiView,
    UserApiView,
)

urlpatterns = [
    path("users/<int:user_id>/", UserApiView.as_view(), name="get-user"),
    path(
        "users/<int:user_id>/create-user/",
        CreateUserApiView.as_view(),
        name="create-user",
    ),
    path(
        "users/<int:user_id>/create-admin/",
        CreateAdminApiView.as_view(),
        name="create-admin",
    ),
]
