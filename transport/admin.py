from tokenize import Single
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
    raw_id_fields = ("user",)
    list_display = (
        "vehicle_make",
        "type_of_car",
        "price_per_day",
        "additional_price_with_a_driver",
        "date_posted",
    )
    list_filter = (
        "vehicle_make",
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
        "user__email",
        "user__first_name",
        "user__last_name",
        "type_of_car",
        "vehicle_make",
    )
    ordering = (
        "date_posted",
        "price_per_day",
        "additional_price_with_a_driver",
    )


class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "starting_point",
        "destination",
        "date_posted",
        "is_admin_entry",
        "paid",
    )
    list_filter = (
        "starting_point",
        "destination",
        "date_posted",
        "paid",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "starting_point",
                    "destination",
                    "number_of_people",
                    "flight_types",
                    "is_admin_entry",
                    "user_has_ordered",
                    "paid",
                    "reviewing",
                    "email_sent",
                    "cancelled",
                )
            },
        ),
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "starting_point",
        "destination",
    )
    ordering = (
        "date_posted",
        "reviewing",
        "cancelled",
        "email_sent",
        "paid",
    )


class GeneralTransferAdmin(admin.ModelAdmin):
    list_display = ("starting_point", "destination", "date_posted", "is_train")
    list_filter = (
        "starting_point",
        "destination",
        "date_posted",
        "is_train",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "starting_point",
                    "destination",
                    "is_train",
                )
            },
        ),
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "starting_point",
        "destination",
    )
    ordering = ("date_posted", "is_train")


admin.site.register(Flight, FlightAdmin)
admin.site.register(GeneralTransfers, GeneralTransferAdmin)
admin.site.register(Transportation, TransportationAdmin)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(SaveTransportation)
