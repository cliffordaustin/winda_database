from dataclasses import fields
from recommended_trip.models import *
from django_filters import rest_framework as filters


class RecommendedTripFilter(filters.FilterSet):
    honeymoon = filters.BooleanFilter(field_name="honeymoon")
    family = filters.BooleanFilter(field_name="family")
    friends = filters.BooleanFilter(field_name="friends")
    couples = filters.BooleanFilter(field_name="couples")
    beach = filters.BooleanFilter(field_name="beach")
    game = filters.BooleanFilter(field_name="game")
    caves = filters.BooleanFilter(field_name="caves")
    surfing = filters.BooleanFilter(field_name="surfing")
    tropical = filters.BooleanFilter(field_name="tropical")
    camping = filters.BooleanFilter(field_name="camping")
    hiking = filters.BooleanFilter(field_name="hiking")
    mountain = filters.BooleanFilter(field_name="mountain")
    cabin = filters.BooleanFilter(field_name="cabin")
    lake = filters.BooleanFilter(field_name="lake")
    desert = filters.BooleanFilter(field_name="desert")
    treehouse = filters.BooleanFilter(field_name="treehouse")
    boat = filters.BooleanFilter(field_name="boat")
    creative_space = filters.BooleanFilter(field_name="creative_space")

    class Meta:
        model = SingleTrip
        fields = [
            "honeymoon",
            "family",
            "friends",
            "couples",
            "beach",
            "game",
            "caves",
            "surfing",
            "tropical",
            "camping",
            "hiking",
            "mountain",
            "cabin",
            "lake",
            "desert",
            "treehouse",
            "boat",
            "creative_space",
        ]
