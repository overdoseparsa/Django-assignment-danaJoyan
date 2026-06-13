from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dana.trasnport import permissions
from dana.trasnport.exceptions import PermissionDenied
from dana.trasnport.models import Transport, Bus, Seat
from dana.users.models import Admin


class TransportFilter(filters.FilterSet):
    
    bus = filters.NumberFilter(field_name='bus__id')
    bus_name = filters.CharFilter(field_name='bus__name', lookup_expr='icontains')
    
    min_seats = filters.NumberFilter(field_name='seat__count', lookup_expr='gte', method='filter_min_seats')
    max_seats = filters.NumberFilter(field_name='seat__count', lookup_expr='lte', method='filter_max_seats')
    
    search = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('name', 'name'),
            ('bus__name', 'bus_name'),
        )
    )
    
    def filter_min_seats(self, queryset, name, value):
        from django.db.models import Count
        return queryset.annotate(seat_count=Count('seat')).filter(seat_count__gte=value)
    
    def filter_max_seats(self, queryset, name, value):
        from django.db.models import Count
        return queryset.annotate(seat_count=Count('seat')).filter(seat_count__lte=value)
    
    class Meta:
        model = Transport
        fields = {
            'bus__id': ['exact'],
            'bus__name': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
        }


