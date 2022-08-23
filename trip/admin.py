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
    raw_id_fields = ("user", "trip")
    search_fields = ("user__email", "user__first_name", "user__last_name", "trip__name")
    ordering = ("updated_at",)
    list_display = (
        "user",
        "trip",
        "starting_date",
        "guests",
        "non_residents",
        "created_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "trip",
                    "starting_date",
                    "guests",
                    "non_residents",
                    "message",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "reviewing",
                    "email_sent",
                    "cancelled",
                    "paid",
                )
            },
        ),
    )


admin.site.register(BookedTrip, BookedTripAdmin)

admin.site.register(Trip, TripAdmin)

admin.site.register(GroupTrip, GroupTripAdmin)
