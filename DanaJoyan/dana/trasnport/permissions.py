from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from dana.users.jwt_service import get_user_id_from_access_token
from dana.users.selectors import get_single_admin

from .exceptions import PermissionDenied


class ISAdminUser(BasePermission):
    def has_permission(self, request: Request, view):
        print("user id is ", request.headers)
        if request.headers.get("Authorization") is None:
            request.admin_user = None
            raise PermissionDenied("Authentication credentials were not provided")
        user_id = get_user_id_from_access_token(request.headers.get("Authorization"))
        if user_id is None:
            request.admin_user = None
            raise PermissionDenied("Authentication credentials were not provided")
        print("user_id", user_id)
        request.admin_user = get_single_admin(user_id)
        print("admin_user", request.admin_user)
        if request.admin_user is None:
            raise PermissionDenied("User is not an admin")

        return True
