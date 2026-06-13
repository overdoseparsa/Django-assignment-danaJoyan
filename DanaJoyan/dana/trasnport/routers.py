from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dana.trasnport import admin, permissions
from dana.trasnport.exceptions import PermissionDenied
from dana.trasnport.models import (
    Bus,
    Company,
)
from dana.users.models import Admin

"""
swagger Compony Create
"""


class CompanySerializerForSwagger(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]


@extend_schema_view(
    create=extend_schema(
        summary="Create a new company",
        description="Create a new company by an admin user. Author will be set automatically.",
        request=CompanySerializerForSwagger,
        responses={
            201: CompanySerializerForSwagger,
            400: "Bad Request",
            403: "Forbidden",
        },
        tags=["Transport Companies"],
        # parameters رو میتونی حذف کنی چون گلوبال تنظیم شده
    ),
    update=extend_schema(
        summary="Update a company",
        description="Update a company. Only the author admin can update.",
        responses={
            200: CompanySerializerForSwagger,
            403: "Permission denied",
            404: "Not found",
        },
        tags=["Transport Companies"],
    ),
    partial_update=extend_schema(
        summary="Partially update a company",
        description="Partially update a company. Only the author admin can update.",
        tags=["Transport Companies"],
    ),
    destroy=extend_schema(
        summary="Delete a company",
        description="Delete a company. Only the author admin can delete.",
        responses={204: "No Content", 403: "Permission denied", 404: "Not found"},
        tags=["Transport Companies"],
    ),
    list=extend_schema(
        summary="List all companies",
        description="Get a list of all companies. Requires admin authentication.",
        tags=["Transport Companies"],
    ),
    retrieve=extend_schema(
        summary="Get a specific company",
        description="Get details of a specific company by ID.",
        tags=["Transport Companies"],
    ),
)
class CompanyViewSet(ModelViewSet):
    class CompanySerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = "__all__"
            read_only_fields = ["author", "created_at", "updated_at"]

        def create(self, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            validated_data["author"] = admin_user
            return super().create(validated_data)

        def update(self, instance, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            if admin_user == instance.author:
                return super().update(instance, validated_data)

            raise PermissionDenied("You do not have permission to update this company")

        def partial_update(self, instance, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            if admin_user == instance.author:
                return super().partial_update(instance, validated_data)
            raise PermissionDenied("You do not have permission to update this company")

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.ISAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["admin_user"] = getattr(self.request, "admin_user", None)
        return context

    def perform_destroy(self, instance):
        admin_user = getattr(self.request, "admin_user", None)

        if admin_user != instance.author:
            raise PermissionDenied("You do not have permission to delete this company")

        instance.delete()


"""
Bus api viewset
"""


class BusSerializerForSwagger(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]


@extend_schema_view(
    create=extend_schema(
        summary="Create a new bus",
        description="Create a new bus by an admin user. Author will be set automatically.",
        request=BusSerializerForSwagger,
        responses={
            201: BusSerializerForSwagger,
            400: "Bad Request",
            403: "Forbidden",
        },
        tags=["Transport Buses"],
        # parameters رو میتونی حذف کنی چون گلوبال تنظیم شده
    ),
    update=extend_schema(
        summary="Update a bus",
        description="Update a bus. Only the author admin can update.",
        responses={
            200: BusSerializerForSwagger,
            403: "Permission denied",
            404: "Not found",
        },
        tags=["Transport Buses"],
    ),
    partial_update=extend_schema(
        summary="Partially update a bus",
        description="Partially update a bus. Only the author admin can update.",
        tags=["Transport Buses"],
    ),
    destroy=extend_schema(
        summary="Delete a bus",
        description="Delete a bus. Only the author admin can delete.",
        responses={204: "No Content", 403: "Permission denied", 404: "Not found"},
        tags=["Transport Buses"],
    ),
    list=extend_schema(
        summary="List all buses",
        description="Get a list of all buses. Requires admin authentication.",
        tags=["Transport Buses"],
    ),
    retrieve=extend_schema(
        summary="Get a specific bus",
        description="Get details of a specific bus by ID.",
        tags=["Transport Buses"],
    ),
)
class BusApiviewset(ModelViewSet):
    class BusSerializerForSwagger(serializers.ModelSerializer):
        class Meta:
            model = Bus
            fields = "__all__"
            read_only_fields = ["author", "created_at", "updated_at"]

        def create(self, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            validated_data["author"] = admin_user
            return super().create(validated_data)

        def update(self, instance, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            if admin_user == instance.author:
                return super().update(instance, validated_data)

            raise PermissionDenied("You do not have permission to update this company")

        def partial_update(self, instance, validated_data):
            admin_user: Admin = self.context.get("admin_user")
            assert admin_user is not None, "admin_user is required"
            if admin_user == instance.author:
                return super().partial_update(instance, validated_data)
            raise PermissionDenied("You do not have permission to update this company")

    queryset = Bus.objects.all()
    serializer_class = BusSerializerForSwagger
    permission_classes = [permissions.ISAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["admin_user"] = getattr(self.request, "admin_user", None)
        return context

    def perform_destroy(self, instance):
        admin_user = getattr(self.request, "admin_user", None)

        if admin_user != instance.author:
            raise PermissionDenied("You do not have permission to delete this company")

        instance.delete()
