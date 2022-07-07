from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class TransportationImageInline(admin.TabularInline):
    model = TransportationImage
    extra = 1


class DriverOperatesWithinInline(admin.TabularInline):
    model = DriverOperatesWithin
    extra = 1


class IncludedInPriceInline(admin.TabularInline):
    model = IncludedInPrice
    extra = 1


class TransportationAdmin(admin.ModelAdmin):
    inlines = (
        TransportationImageInline,
        DriverOperatesWithinInline,
        IncludedInPriceInline,
    )
    list_display = (
        "user",
        "type_of_car",
        "price_per_day",
        "additional_price_with_a_driver",
        "date_posted",
    )
    list_filter = (
        "price_per_day",
        "additional_price_with_a_driver",
        "date_posted",
        "type_of_car",
        "vehicle_make",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "type_of_car",
                    "vehicle_make",
                    "price_per_day",
                    "additional_price_with_a_driver",
                    "capacity",
                    "bags",
                    "transmission",
                    "is_active",
                )
            },
        ),
        (
            "Comfort",
            {
                "fields": [
                    "has_air_condition",
                    "four_wheel_drive",
                    "open_roof",
                ]
            },
        ),
        (
            "Policies",
            {
                "fields": [
                    "policy",
                ]
            },
        ),
    )

    search_fields = (
        "user",
        "type_of_car",
        "price_per_day",
        "additional_price_with_a_driver",
        "date_posted",
    )
    ordering = (
        "date_posted",
        "price_per_day",
        "additional_price_with_a_driver",
    )


admin.site.register(Transportation, TransportationAdmin)

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(SaveTransportation)
