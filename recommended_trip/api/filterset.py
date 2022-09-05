from dataclasses import fields
from random import choices
from recommended_trip.models import *
from django_filters import rest_framework as filters


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecommendedTripFilter(filters.FilterSet):
    pricing_type = filters.ChoiceFilter(choices=PRICING_TYPE, field_name="pricing_type")
    area_covered = filters.CharFilter(
        field_name="area_covered", lookup_expr="icontains"
    )
    old_price = filters.NumberFilter(method="deals")

    def deals(self, queryset, name, value):
        if value:
            return queryset.filter(old_price__gt=0)
        return queryset

    class Meta:
        model = SingleTrip
        exclude = ["stop_at", "countries_covered"]
