from django.contrib import admin
from .models import *

from nested_inline.admin import (
    NestedStackedInline,
    NestedModelAdmin,
    NestedTabularInline,
)


# Curated trip admin


class CuratedTripImageInline(NestedTabularInline):
    model = CuratedTripImage
    extra = 1


class SimilarTripsInline(NestedTabularInline):
    model = SimilarTrips.curated_trip.through
    extra = 1


class CuratedTripLocationsInline(NestedStackedInline):
    model = CuratedTripLocations
    extra = 1


class ItineraryAccommodationInline(NestedStackedInline):
    model = ItineraryAccommodation
    raw_id_fields = ("stay",)
    extra = 1


class IncludedItineraryActivityInline(NestedStackedInline):
    model = IncludedItineraryActivity
    raw_id_fields = ("activity",)
    extra = 1


class OptionalItineraryActivityInline(NestedStackedInline):
    model = OptionalItineraryActivity
    extra = 1


class ItineraryTransportInline(NestedStackedInline):
    model = ItineraryTransport
    extra = 1


class ItineraryLocationInline(NestedStackedInline):
    model = ItineraryLocation
    extra = 1


class ItineraryInline(NestedStackedInline):
    model = Itinerary
    inlines = [
        ItineraryLocationInline,
        ItineraryTransportInline,
        IncludedItineraryActivityInline,
        OptionalItineraryActivityInline,
        ItineraryAccommodationInline,
    ]
    extra = 1


class CuratedTripAdmin(NestedModelAdmin):
    inlines = (
        CuratedTripLocationsInline,
        CuratedTripImageInline,
        ItineraryInline,
        SimilarTripsInline,
    )
    raw_id_fields = ("user",)

    list_display = (
        "user",
        "name",
        "total_number_of_days",
        "number_of_countries",
        "max_number_of_people",
        "created_at",
        "updated_at",
        "is_active",
    )

    list_filter = (
        "is_active",
        "total_number_of_days",
        "number_of_countries",
        "max_number_of_people",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                    "total_number_of_days",
                    "number_of_countries",
                    "max_number_of_people",
                    "trip_is_carbon_neutral",
                    "essential_information",
                    "description",
                )
            },
        ),
        (
            "Prices",
            {
                "fields": (
                    "old_price",
                    "price",
                    "price_non_resident",
                    "pricing_type",
                )
            },
        ),
        (
            "Categories",
            {
                "fields": (
                    "weekend_getaway",
                    "road_trip",
                    "day_game_drives",
                    "cultural",
                    "romantic",
                    "culinary",
                    "day_trips",
                    "community_owned",
                    "off_grid",
                    "solo_getaway",
                    "wellness",
                    "unconventional_safaris",
                    "walking_hiking",
                    "shopping",
                    "art",
                    "watersports",
                    "sailing",
                    "night_game_drives",
                    "sustainable",
                    "all_female",
                    "family",
                    "groups",
                    "luxury",
                    "budget",
                    "mid_range",
                    "beach",
                    "short_getaways",
                    "cross_country",
                    "lake",
                    "park_conservancies",
                )
            },
        ),
        (
            "Others",
            {"fields": ("is_active",)},
        ),
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


admin.site.register(CuratedTrip, CuratedTripAdmin)
