from django_filters import rest_framework as filters
from rest_framework import fields
from lodging.models import Stays, TYPE_OF_STAY, PRICING_TYPE
from django.db.models import Q


def multiple_search(queryset, name, value):
    queryset = queryset.filter(
        Q(best_describes_lodge__in=value)
        | Q(best_describes_house__in=value)
        | Q(best_describes_unique_space__in=value)
        | Q(best_describes_campsite__in=value)
        | Q(best_describes_boutique_hotel__in=value)
    )
    return queryset


class ItemInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class NumberInFilter(filters.BaseCSVFilter, filters.NumberFilter):
    pass


class StayFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="lte")
    type_of_stay = filters.ChoiceFilter(
        field_name="type_of_stay", lookup_expr="icontains", choices=TYPE_OF_STAY
    )
    # amenities = filters.CharFilter(field_name="amenities", lookup_expr="icontains")

    class Meta:
        model = Stays
        fields = [
            "min_price",
            "max_price",
            "min_rooms",
            "max_rooms",
            "type_of_stay",
            # "amenities",
        ]
