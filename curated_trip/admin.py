from django.contrib import admin
from .models import *


# Curated trip admin


class CuratedTripImageInline(admin.TabularInline):
    model = CuratedTripImage
    extra = 1


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1


class FrequentlyAskedQuestionInline(admin.TabularInline):
    model = FrequentlyAskedQuestion
    extra = 1


class StayTripInline(admin.TabularInline):
    raw_id_fields = ("stay",)
    model = StayTrip
    extra = 1


class ActivityTripInline(admin.TabularInline):
    raw_id_fields = ("activity",)
    model = ActivityTrip
    extra = 1


class TransportTripInline(admin.TabularInline):
    raw_id_fields = ("transport",)
    model = TransportationTrip
    extra = 1


class CuratedTripAdmin(admin.ModelAdmin):
    inlines = (
        CuratedTripImageInline,
        ItineraryInline,
        FrequentlyAskedQuestionInline,
        StayTripInline,
        ActivityTripInline,
        TransportTripInline,
    )
    raw_id_fields = ("user",)

    list_display = (
        "user",
        "name",
        "total_number_of_days",
        "created_at",
        "updated_at",
        "is_active",
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
                    "essential_information",
                    "description",
                    "pricing_type",
                )
            },
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
                    "beachfront",
                    "all_female_owned",
                    "culinary",
                    "solo_experience",
                    "shopping",
                    "community_owned",
                    "natural_and_wildlife",
                    "group_getaway",
                    "riverside",
                    "day_trip",
                    "off_grid",
                    "beautiful_views",
                    "quirky",
                    "conservancies",
                    "wellness",
                    "active_adventure",
                    "farmstay",
                    "cycling",
                    "game",
                    "romantic_getaway",
                    "active",
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
                )
            },
        ),
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "stay_trip__stay__name",
        "stay_trip__stay__property_name",
        "activity_trip__activity__name",
        "transport_trip__transport__vehicle_make",
        "transport_trip__transport__type_of_car",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


admin.site.register(CuratedTrip, CuratedTripAdmin)


# User trip admin
class UserStayTripInline(admin.TabularInline):
    raw_id_fields = ("stay",)
    model = UserStayTrip
    extra = 1


class UserActivityTripInline(admin.TabularInline):
    raw_id_fields = ("activity",)
    model = UserActivityTrip
    extra = 1


class UserTransportTripInline(admin.TabularInline):
    raw_id_fields = ("transport",)
    model = UserTransportTrip
    extra = 1


class UserTripAdmin(admin.ModelAdmin):
    inlines = (
        UserStayTripInline,
        UserActivityTripInline,
        UserTransportTripInline,
    )
    raw_id_fields = ("user", "trips")

    list_display = ("user", "name", "created_at", "updated_at")

    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "trips",
                    "name",
                )
            },
        ),
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "user_stay_trip__stay__name",
        "user_stay_trip__stay__property_name",
        "user_activity_trip__activity__name",
        "user_transport_trip__transport__vehicle_make",
        "user_transport_trip__transport__type_of_car",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


class UserTripsAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

    list_display = ("user", "name", "created_at", "updated_at", "paid")

    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                    "paid",
                )
            },
        ),
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "trip__user_stay_trip__stay__name",
        "trip__user_stay_trip__stay__property_name",
        "trip__user_activity_trip__activity__name",
        "trip__user_transport_trip__transport__vehicle_make",
        "trip__user_transport_trip__transport__type_of_car",
    )

    ordering = (
        "created_at",
        "updated_at",
    )


admin.site.register(UserTrips, UserTripsAdmin)
admin.site.register(UserTrip, UserTripAdmin)
