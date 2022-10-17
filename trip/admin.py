from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# class TripImageInline(admin.TabularInline):
#     model = TripImage
#     extra = 1


# class GroupTripImageInline(admin.TabularInline):
#     model = GroupTripImage
#     extra = 1


class TripAdmin(admin.ModelAdmin):

    search_fields = ("user__email",)
    ordering = ("updated_at",)


class GroupTripAdmin(admin.ModelAdmin):

    search_fields = ("user__email", "name")
    ordering = ("updated_at",)


class BookedTripAdmin(admin.ModelAdmin):
    raw_id_fields = ("trip",)
    search_fields = ("trip__name",)
    ordering = ("updated_at",)
    list_display = (
        "trip_name",
        "starting_date",
        "guests",
        "non_residents",
        "first_name",
        "last_name",
        "email",
        "phone",
        "created_at",
        "paid",
        "booking_request",
    )

    def trip_name(self, obj):
        return obj.trip.name if obj.trip else None

    list_filter = ("booking_request", "paid")

    fieldsets = (
        (
            "Booking Details",
            {
                "fields": (
                    "trip",
                    "starting_date",
                    "guests",
                    "non_residents",
                    "message",
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
                    "reviewing",
                    "email_sent",
                    "cancelled",
                    "paid",
                )
            },
        ),
    )

    ordering = ("created_at",)


admin.site.register(BookedTrip, BookedTripAdmin)

admin.site.register(Trip, TripAdmin)

admin.site.register(GroupTrip, GroupTripAdmin)
