from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserApp
from .selectors import get_user
from .services import create_admin, create_user


class UserApiView(APIView):
    """
    API view for retrieving user information.
    """

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserApp
            fields = [
                "user_id",
                "username",
                "user_email",
            ]

    output_serializer = OutputSerializer

    def get_output_serializer(self, user):
        return self.output_serializer(user)

    @extend_schema(responses=OutputSerializer)
    def get(self, request, user_id: int):
        user = get_user(user_id)
        serializer = self.get_output_serializer(user)
        return Response(serializer.data)


class CreateUserApiView(APIView):
    """
    API view for creating a user.
    """

    def post(self, request, user_id: int):
        try:
            user = create_user(user_id=user_id)
        except UserApp.DoesNotExist:
            return Response(
                {"detail": "UserApp not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": f"User created successfully {user}"},
            status=status.HTTP_201_CREATED,
        )


class CreateAdminApiView(APIView):
    """
    API view for creating an admin.
    """

    def post(self, request, user_id: int):
        try:
            user = create_admin(user_id=user_id)
        except UserApp.DoesNotExist:
            return Response(
                {"detail": "UserApp not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": f"User created successfully {user}"},
            status=status.HTTP_201_CREATED,
        )
