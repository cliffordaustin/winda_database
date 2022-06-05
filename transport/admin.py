from django.contrib import admin
from .models import Transportation, TransportationImage, Views, Cart, Order, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class TransportationImageInline(admin.TabularInline):
    model = TransportationImage
    extra = 1


class TransportationAdmin(admin.ModelAdmin):
    inlines = (TransportationImageInline,)
    list_display = ("user", "type_of_car", "price", "price_per_day", "date_posted")
    list_filter = (
        "price",
        "price_per_day",
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
                    "vehicle_plate",
                    "vehicle_make",
                    "vehicle_color",
                    "price",
                    "price_per_day",
                )
            },
        ),
        (
            "Comfort",
            {
                "fields": [
                    "has_air_condition",
                    "open_roof",
                ]
            },
        ),
        (
            "Entertainment",
            {
                "fields": [
                    "fm_radio",
                    "cd_player",
                    "bluetooth",
                    "audio_input",
                    "cruise_control",
                ]
            },
        ),
        (
            "Safety",
            {
                "fields": [
                    "overhead_passenger_airbag",
                    "side_airbag",
                    "power_locks",
                    "power_mirrors",
                    "power_windows",
                    "safety_tools",
                ]
            },
        ),
        (
            "Other",
            {"fields": ["dropoff_city", "dropoff_country"]},
        ),
    )

    search_fields = ("user", "type_of_car", "price", "price_per_day", "date_posted")
    ordering = ("date_posted", "price", "price_per_day")


admin.site.register(Transportation, TransportationAdmin)

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
