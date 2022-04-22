from django_filters import rest_framework as filters
from rest_framework import fields
from lodging.models import Stays, TYPE_OF_STAY, PRICING_TYPE
from django.db.models import Q
from lodging.models import Review


RATES = (("1", "1"), ("2", "2"), ("3" "3"), ("4", "4"), ("5", "5"))


def multiple_search(queryset, name, value):
    queryset = queryset.filter(
        Q(best_describes_lodge__overlap=value)
        | Q(best_describes_house__overlap=value)
        | Q(best_describes_unique_space__overlap=value)
        | Q(best_describes_campsite__overlap=value)
        | Q(best_describes_boutique_hotel__overlap=value)
    )
    return queryset


class CharInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class NumberInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class StayFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="lte")
    type_of_stay = CharInFilter(field_name="type_of_stay", lookup_expr="in")
    theme = CharInFilter(label="Travel Theme", method=multiple_search)
    amenities = CharInFilter(field_name="ammenities", lookup_expr="overlap")
    # theme = CharInFilter(
    #     field_name="best_describes_house", lookups=["overlap", "icontains"]
    # )

    class Meta:
        model = Stays
        fields = [
            "min_price",
            "max_price",
            "min_rooms",
            "max_rooms",
            "type_of_stay",
            "theme",
            "amenities",
        ]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = Review
        fields = ["rate"]