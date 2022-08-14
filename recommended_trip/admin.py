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
    raw_id_fields = ("user", "stay", "activity", "transport")

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

    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                    "area_covered",
                    "total_number_of_days",
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
            "Tags",
            {
                "fields": (
                    "honeymoon",
                    "cultural",
                    "weekend_getaway",
                    "road_trip",
                    "hiking",
                    "beach",
                    "game",
                    "romantic_getaway",
                    "active",
                    "cycling",
                    "lake",
                    "walking",
                    "family",
                    "couples",
                    "friends",
                    "caves",
                    "surfing",
                    "tropical",
                    "camping",
                    "mountain",
                    "cabin",
                    "desert",
                    "treehouse",
                    "boat",
                    "creative_space",
                )
            },
        ),
        (
            "Others",
            {
                "fields": (
                    "is_active",
                    "starting_location",
                    "ending_location",
                    "country",
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


admin.site.register(SingleTrip, SingleTripAdmin)
