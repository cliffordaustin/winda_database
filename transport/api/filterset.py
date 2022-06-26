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
    type_of_car = CharInFilter(field_name="type_of_car", lookup_expr="in")
    vehicle_make = filters.CharFilter(
        field_name="vehicle_make", lookup_expr="icontains"
    )
    has_air_condition = filters.BooleanFilter(field_name="has_air_condition")
    fm_radio = filters.BooleanFilter(field_name="fm_radio")
    cd_player = filters.BooleanFilter(field_name="cd_player")
    bluetooth = filters.BooleanFilter(field_name="bluetooth")
    audio_input = filters.BooleanFilter(field_name="audio_input")
    cruise_control = filters.BooleanFilter(field_name="cruise_control")
    overhead_passenger_airbag = filters.BooleanFilter(
        field_name="overhead_passenger_airbag"
    )
    side_airbag = filters.BooleanFilter(field_name="side_airbag")
    power_locks = filters.BooleanFilter(field_name="power_locks")
    power_mirrors = filters.BooleanFilter(field_name="power_mirrors")
    power_window = filters.BooleanFilter(field_name="power_windows")
    open_roof = filters.BooleanFilter(field_name="open_roof")
    safety_tools = CharInFilter(field_name="safety_tools", lookup_expr="overlap")

    class Meta:
        model = Transportation
        fields = [
            "min_price",
            "max_price",
            "type_of_car",
            "vehicle_make",
            "has_air_condition",
            "fm_radio",
            "cd_player",
            "bluetooth",
            "audio_input",
            "cruise_control",
            "overhead_passenger_airbag",
            "side_airbag",
            "power_locks",
            "power_mirrors",
            "power_window",
            "open_roof",
            "safety_tools",
        ]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = Review
        fields = ["rate"]
