from rest_framework.exceptions import APIException  # توجه: APIException با حروف بزرگ


class PermissionDenied(APIException):
    pass
