from django.contrib import admin
from .models import *


class SingleTripImageInline(admin.TabularInline):
    model = SingleTripImage
    extra = 1


class SingleTripAdmin(admin.ModelAdmin):
    inlines = (SingleTripImageInline,)

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
            {"fields": ("user", "name", "description")},
        ),
        (
            "Stay",
            {
                "fields": (
                    "stay",
                    "stay_plan",
                    "stay_num_of_adults",
                    "stay_num_of_children",
                    "stay_non_resident",
                    "nights",
                )
            },
        ),
        (
            "Experience",
            {
                "fields": (
                    "activity",
                    "activity_pricing_type",
                    "activity_number_of_people",
                    "activity_number_of_sessions",
                    "activity_number_of_groups",
                    "activity_non_resident",
                )
            },
        ),
        (
            "Transport",
            {
                "fields": (
                    "transport",
                    "starting_point",
                    "user_need_a_driver",
                )
            },
        ),
        (
            "Tags",
            {
                "fields": (
                    "honeymoon",
                    "familiy",
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
