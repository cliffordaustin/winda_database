from calendar import c
from django_filters import rest_framework as filters
from rest_framework import fields
from django.db.models import Q
from transport.models import *


RATES = (("1", "1"), ("2", "2"), ("3" "3"), ("4", "4"), ("5", "5"))


class CharInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class TransportationFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="lte")
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    max_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="lte")
    min_bags = filters.NumberFilter(field_name="bags", lookup_expr="gte")
    max_bags = filters.NumberFilter(field_name="bags", lookup_expr="lte")
    transmission = filters.ChoiceFilter(
        field_name="transmission", choices=TYPE_OF_TRANSMISSION
    )
    type_of_car = CharInFilter(field_name="type_of_car", lookup_expr="in")
    vehicle_make = filters.CharFilter(
        field_name="vehicle_make", lookup_expr="icontains"
    )
    has_air_condition = filters.BooleanFilter(field_name="has_air_condition")
    four_wheel_drive = filters.BooleanFilter(field_name="four_wheel_drive")
    open_roof = filters.BooleanFilter(field_name="open_roof")

    class Meta:
        model = Transportation
        fields = [
            "min_price",
            "max_price",
            "min_capacity",
            "min_bags",
            "max_bags",
            "transmission",
            "type_of_car",
            "vehicle_make",
            "has_air_condition",
            "four_wheel_drive",
            "open_roof",
        ]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = Review
        fields = ["rate"]
