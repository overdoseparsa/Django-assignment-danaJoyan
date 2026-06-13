import django_filters as filters
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
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
    Seat,
    Transport,
)
from dana.users.models import Admin

from .services import create_transport

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


"""
Seat api
"""


class SeatSerializerForSwagger(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]


@extend_schema_view(
    create=extend_schema(
        summary="Create a new Seat",
        description="Create a new Seat by an admin user. Author will be set automatically.",
        request=SeatSerializerForSwagger,
        responses={
            201: SeatSerializerForSwagger,
            400: "Bad Request",
            403: "Forbidden",
        },
        tags=["Transport Seats"],
        # parameters رو میتونی حذف کنی چون گلوبال تنظیم شده
    ),
    update=extend_schema(
        summary="Update a Seat",
        description="Update a Seat. Only the author admin can update.",
        request=SeatSerializerForSwagger,
        responses={
            200: SeatSerializerForSwagger,
            403: "Permission denied",
            404: "Not found",
        },
        tags=["Transport Seats"],
    ),
    partial_update=extend_schema(
        summary="Partially update a Seat",
        description="Partially update a Seat. Only the author admin can update.",
        tags=["Transport Seats"],
    ),
    destroy=extend_schema(
        summary="Delete a Seat",
        description="Delete a Seat. Only the author admin can delete.",
        responses={204: "No Content", 403: "Permission denied", 404: "Not found"},
        tags=["Transport Seats"],
    ),
    list=extend_schema(
        summary="List all Seats",
        description="Get a list of all Seats. Requires admin authentication.",
        tags=["Transport Seats"],
    ),
    retrieve=extend_schema(
        summary="Get a specific Seat",
        description="Get details of a specific Seat by ID.",
        tags=["Transport Seats"],
    ),
)
class SeatApiviewset(ModelViewSet):
    class SeatSerializerForSwagger(serializers.ModelSerializer):
        class Meta:
            model = Seat
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

    queryset = Seat.objects.all()
    serializer_class = SeatSerializerForSwagger
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
Trasport Create
"""


class TransportApiview(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        bus = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all())
        seat = serializers.PrimaryKeyRelatedField(
            queryset=Seat.objects.all(), many=True
        )

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transport
            fields = "__all__"

    permission_classes = [permissions.ISAdminUser]

    @extend_schema(
        summary="Create a new transport",
        description="Create a new transport record. Requires admin authentication.",
        request=InputSerializer,
        responses={
            201: OutputSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
        },
        tags=["Transport create"],
        parameters=[
            OpenApiParameter(
                name="Authorization",
                location="header",
                description="Bearer <access_token>",
                required=True,
                type=str,
            )
        ],
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid():
            try:
                transport = create_transport(
                    serializer.validated_data, request.admin_user
                )
                output_serializer = self.OutputSerializer(transport)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="List all transports",
        description="Get list of all transport records with advanced filtering.",
        responses={200: OutputSerializer(many=True)},
        tags=["Transport Retrieval"],
        parameters=[
            OpenApiParameter(
                name="Authorization",
                location="header",
                description="Bearer <access_token>",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="bus",
                location="query",
                description="Filter by bus ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="bus_name",
                location="query",
                description="Filter by bus name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="name",
                location="query",
                description="Exact name filter",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                location="query",
                description="Search in name (contains)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="min_seats",
                location="query",
                description="Minimum number of seats",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="max_seats",
                location="query",
                description="Maximum number of seats",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="ordering",
                location="query",
                description="Order by: created_at, -created_at, name, -name",
                required=False,
                type=str,
            ),
        ],
    )
    def get(self, request):
        queryset = Transport.objects.all()

        filter_backend = DjangoFilterBackend()
        filtered_queryset = filter_backend.filter_queryset(request, queryset, view=self)

        page_number = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        try:
            page_size = int(page_size)
            if page_size > 100:
                page_size = 100
        except ValueError:
            page_size = 10

        paginator = Paginator(filtered_queryset, page_size)

        try:
            paginated_queryset = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        serializer = self.OutputSerializer(paginated_queryset, many=True)

        return Response(
            {
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": paginated_queryset.number,
                "page_size": page_size,
                "next": paginated_queryset.has_next(),
                "previous": paginated_queryset.has_previous(),
                "results": serializer.data,
            }
        )
