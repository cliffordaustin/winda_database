from django_filters import rest_framework as filters
from activities.models import Activities, Review

RATES = (("1", "1"), ("2", "2"), ("3" "3"), ("4", "4"), ("5", "5"))


class CharInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class ActivitiesFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_non_resident", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_non_resident", lookup_expr="lte")
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    max_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="lte")
    type_of_activities = CharInFilter(
        field_name="type_of_activities", lookup_expr="overlap"
    )

    class Meta:
        model = Activities
        # fields = [
        #     "min_price",
        #     "max_price",
        #     "min_capacity",
        #     "max_capacity",
        #     "type_of_activities",
        #     "gear_or_equipments",
        # ]

        exclude = [
            "type_of_activities",
            "equipments_required_by_user_to_bring",
            "equipments_provided",
            "tags",
        ]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = Review
        fields = ["rate"]
