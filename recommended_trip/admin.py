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


class SingleTripAdmin(admin.ModelAdmin):
    inlines = (SingleTripImageInline, TripHighlightInline, RecommendedMonthsInline)

    list_display = (
        "user",
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {"fields": ("user", "name", "area_covered", "description", "pricing_type")},
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
        ("Others", {"fields": ("is_active",)}),
    )

    search_fields = (
        "user",
        "name",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


admin.site.register(SingleTrip, SingleTripAdmin)
