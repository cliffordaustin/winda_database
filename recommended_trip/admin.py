from django.contrib import admin
from .models import *


class SingleTripImageInline(admin.TabularInline):
    model = SingleTripImage
    extra = 1


class RecommendedMonthsInline(admin.TabularInline):
    model = RecommendedMonths
    extra = 1


class TripHighlightInline(admin.TabularInline):
    model = TripHighlight
    extra = 1


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1


class FrequentlyAskedQuestionInline(admin.TabularInline):
    model = FrequentlyAskedQuestion
    extra = 1


class SingleTripAdmin(admin.ModelAdmin):
    inlines = (
        SingleTripImageInline,
        TripHighlightInline,
        ItineraryInline,
        FrequentlyAskedQuestionInline,
    )
    raw_id_fields = (
        "user",
        "stay",
        "activity",
        "transport",
        "flight",
        "general_transfer",
    )

    list_display = (
        "user",
        "name",
        "stay_name",
        "total_number_of_days",
        "experience_name",
        "transport_name",
        "created_at",
        "updated_at",
        "is_active",
    )

    def stay_name(self, obj):
        return obj.stay.name if obj.stay else None

    def experience_name(self, obj):
        return obj.activity.name if obj.activity else None

    def transport_name(self, obj):
        return (
            obj.transport.vehicle_make + " " + obj.transport.type_of_car
            if obj.transport
            else None
        )

    list_filter = ("created_at", "updated_at", "is_active")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                    "area_covered",
                    "countries_covered",
                    "nights",
                    "total_number_of_days",
                    "essential_information",
                    "description",
                    "pricing_type",
                )
            },
        ),
        (
            "Stay",
            {"fields": ("stay",)},
        ),
        (
            "Experience",
            {"fields": ("activity",)},
        ),
        (
            "Transport",
            {"fields": ("transport",)},
        ),
        (
            "Flight",
            {"fields": ("flight",)},
        ),
        (
            "General Transfer",
            {"fields": ("general_transfer",)},
        ),
        (
            "Prices",
            {"fields": ("old_price", "price", "price_non_resident")},
        ),
        (
            "Tags",
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
                    "has_holiday_package",
                    "starting_location",
                    "ending_location",
                    "stop_at",
                )
            },
        ),
    )

    search_fields = (
        "name",
        "stay__name",
        "stay__property_name",
        "activity__name",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


class RequestCustomTripAdmin(admin.ModelAdmin):
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
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "message",
                )
            },
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


class RequestInfoTripAdmin(admin.ModelAdmin):
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


admin.site.register(SingleTrip, SingleTripAdmin)

admin.site.register(RequestCustomTrip, RequestCustomTripAdmin)

admin.site.register(RequestInfo, RequestInfoTripAdmin)
