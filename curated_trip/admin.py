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


class PricePlanAInline(NestedTabularInline):
    model = PricePlanA
    extra = 1


class PricePlanBInline(NestedTabularInline):
    model = PricePlanB
    extra = 1


class PricePlanCInline(NestedTabularInline):
    model = PricePlanC
    extra = 1


# class SimilarTripsInline(NestedTabularInline):
#     model = SimilarTrips.curated_trip.through
#     extra = 1


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
        ItineraryAccommodationInline,
        IncludedItineraryActivityInline,
        OptionalItineraryActivityInline,
        ItineraryTransportInline,
    ]
    extra = 1


def duplicate_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.duplicate()

    message = f"Successfully duplicated {queryset.count()} lodges."
    modeladmin.message_user(request, message)


duplicate_selected.short_description = "Duplicate selected lodges"


class CuratedTripAdmin(NestedModelAdmin):
    inlines = (
        CuratedTripLocationsInline,
        CuratedTripImageInline,
        ItineraryInline,
        PricePlanAInline,
        PricePlanBInline,
        PricePlanCInline,
    )
    actions = [duplicate_selected]
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
            {
                "fields": (
                    "is_active",
                    "valentine_offer",
                )
            },
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


class RequestInfoOnCustomTripAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "created_at",
    )

    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {"fields": ("first_name", "last_name", "email", "message", "trip")},
        ),
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


class BookedTripAdmin(admin.ModelAdmin):
    raw_id_fields = ("trip",)
    search_fields = ("trip__name",)
    ordering = ("updated_at",)
    list_display = (
        "trip_name",
        "starting_date",
        "adults",
        "first_name",
        "last_name",
        "email",
        "phone",
        "created_at",
        "paid",
        "plan",
        "booking_request",
    )

    def trip_name(self, obj):
        return obj.trip.name if obj.trip else None

    list_filter = ("booking_request", "plan", "paid")

    fieldsets = (
        (
            "Booking Details",
            {
                "fields": (
                    "trip",
                    "starting_date",
                    "adults",
                    "message",
                    "plan",
                )
            },
        ),
        (
            "Personal Details",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "booking_request",
                    "cancelled",
                    "paid",
                )
            },
        ),
    )

    ordering = ("created_at",)


class TripWizardAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "number_of_people",
        "locations",
        "tags",
        "month",
        "year",
    )
    ordering = ("number_of_people",)
    search_fields = ("first_name", "last_name", "locations", "month", "year")

    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "number_of_people",
                )
            },
        ),
        (
            "Trip Info",
            {
                "fields": (
                    "locations",
                    "month",
                    "year",
                    "tags",
                )
            },
        ),
    )

    ordering = ("created_at",)


class EbookEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    ordering = ("created_at",)
    search_fields = ("email",)


admin.site.register(CuratedTrip, CuratedTripAdmin)
admin.site.register(BookedTrip, BookedTripAdmin)
admin.site.register(RequestInfoOnCustomTrip, RequestInfoOnCustomTripAdmin)
admin.site.register(TripWizard, TripWizardAdmin)
admin.site.register(EbookEmail, EbookEmailAdmin)
