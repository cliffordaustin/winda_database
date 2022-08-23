from dataclasses import fields
from random import choices
from curated_trip.models import *
from django_filters import rest_framework as filters


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecommendedTripFilter(filters.FilterSet):
    pricing_type = filters.ChoiceFilter(choices=PRICING_TYPE, field_name="pricing_type")
    area_covered = filters.CharFilter(
        field_name="area_covered", lookup_expr="icontains"
    )

    class Meta:
        model = CuratedTrip
        exclude = ["stop_at"]
