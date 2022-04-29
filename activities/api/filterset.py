from django_filters import rest_framework as filters
from activities.models import Activities


class CharInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class ActivitiesFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    type_of_activities = CharInFilter(
        field_name="type_of_activities", lookup_expr="overlap"
    )
    gear_or_equipments = CharInFilter(
        field_name="gear_or_equipments", lookup_expr="overlap"
    )

    class Meta:
        model = Activities
        fields = [
            "min_price",
            "max_price",
            "type_of_activities",
            "gear_or_equipments",
        ]
