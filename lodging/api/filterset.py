from django_filters import rest_framework as filters
from rest_framework import fields
from lodging.models import Stays, TYPE_OF_STAY, PRICING_TYPE
from django.db.models import Q
from lodging.models import Review, Bookings


RATES = (("1", "1"), ("2", "2"), ("3" "3"), ("4", "4"), ("5", "5"))


# def multiple_search(queryset, name, value):
#     queryset = queryset.filter(
#         Q(best_describes_lodge__overlap=value)
#         | Q(best_describes_house__overlap=value)
#         | Q(best_describes_unique_space__overlap=value)
#         | Q(best_describes_campsite__overlap=value)
#         | Q(best_describes_boutique_hotel__overlap=value)
#     )
#     return queryset


class CharInFilter(filters.BaseInFilter, filters.CharFilter):

    pass


class NumberInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class StayFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_non_resident", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_non_resident", lookup_expr="lte")
    min_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = filters.NumberFilter(field_name="rooms", lookup_expr="lte")
    min_bathrooms = filters.NumberFilter(field_name="bathrooms", lookup_expr="gte")
    max_bathrooms = filters.NumberFilter(field_name="bathrooms", lookup_expr="lte")
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    max_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="lte")
    min_beds = filters.NumberFilter(field_name="beds", lookup_expr="gte")
    max_beds = filters.NumberFilter(field_name="beds", lookup_expr="lte")
    type_of_stay = CharInFilter(field_name="type_of_stay", lookup_expr="in")
    pricing_type = filters.ChoiceFilter(field_name="pricing_type", choices=PRICING_TYPE)
    has_holiday_package = filters.BooleanFilter(field_name="has_holiday_package")
    in_homepage = filters.BooleanFilter(field_name="in_homepage")
    has_options = filters.BooleanFilter(field_name="has_options")
    is_kaleidoscope_event = filters.BooleanFilter(field_name="is_kaleidoscope_event")
    # theme = CharInFilter(label="Travel Theme", method=multiple_search)

    class Meta:
        model = Stays
        # fields = [
        #     "min_price",
        #     "max_price",
        #     "min_rooms",
        #     "max_rooms",
        #     "min_bathrooms",
        #     "max_bathrooms",
        #     "min_beds",
        #     "max_beds",
        #     "type_of_stay",
        #     "theme",
        # ]

        exclude = ["tags", "unavailable_dates"]


class BookingsFilter(filters.FilterSet):
    class Meta:
        model = Bookings
        exclude = ["room_type"]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = Review
        fields = ["rate"]
