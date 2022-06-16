from django.contrib import admin
from .models import *


class SingleTripImageInline(admin.TabularInline):
    model = SingleTripImage
    extra = 1


class RecommendedMonthsInline(admin.TabularInline):
    model = RecommendedMonths
    extra = 1


class SingleTripAdmin(admin.ModelAdmin):
    inlines = (SingleTripImageInline, RecommendedMonthsInline)

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
            {"fields": ("user", "name", "description", "price_budget")},
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
            {
                "fields": (
                    "transport",
                    "starting_point",
                )
            },
        ),
        (
            "Tags",
            {
                "fields": (
                    "honeymoon",
                    "family",
                    "couples",
                    "friends",
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
                )
            },
        ),
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
