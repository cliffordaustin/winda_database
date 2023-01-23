from django.contrib import admin
from .models import *
from nested_inline.admin import (
    NestedStackedInline,
    NestedModelAdmin,
    NestedTabularInline,
)


class StayImageInline(NestedTabularInline):
    model = StayImage
    extra = 1


class ExtrasIncludedInline(NestedTabularInline):
    model = ExtrasIncluded
    extra = 1


class FactsInline(NestedTabularInline):
    model = Facts
    extra = 1


class InclusionsInline(NestedTabularInline):
    model = Inclusions
    extra = 1


class TypeOfRoomsImageInline(NestedStackedInline):
    model = TypeOfRoomsImages
    extra = 1
    fk_name = "room"


class TypeOfRoomsAdmin(NestedStackedInline):
    model = TypeOfRooms
    extra = 1
    fk_name = "stay"
    inlines = [TypeOfRoomsImageInline]


class PrivateSafariImagesInline(NestedStackedInline):
    model = PrivateSafariImages
    extra = 1
    fk_name = "private_safari"


class PrivateSafariAdmin(NestedStackedInline):
    model = PrivateSafari
    extra = 1
    fk_name = "stay"
    inlines = [PrivateSafariImagesInline]


class SharedSafariImagesInline(NestedStackedInline):
    model = SharedSafariImages
    extra = 1
    fk_name = "shared_safari"


class SharedSafariAdmin(NestedStackedInline):
    model = SharedSafari
    extra = 1
    fk_name = "stay"
    inlines = [SharedSafariImagesInline]


class AllInclusiveImageInline(NestedStackedInline):
    model = AllInclusiveImages
    extra = 1
    fk_name = "all_inclusive"


class AllInclusiveAdmin(NestedStackedInline):
    model = AllInclusive
    extra = 1
    fk_name = "stay"
    inlines = [AllInclusiveImageInline]


class OtherOptionImagesInline(NestedStackedInline):
    model = OtherOptionImages
    extra = 1
    fk_name = "other_option"


class OtherOptionAdmin(NestedStackedInline):
    model = OtherOption
    extra = 1
    fk_name = "stay"
    inlines = [OtherOptionImagesInline]


# admin.site.register(TypeOfRooms, TypeOfRoomsAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "passengers",
        "phone",
        "from_date",
        "to_date",
        "rooms",
        "type_of_room",
        "adults",
        "confirmation_code",
        "paid",
    )

    list_filter = (
        "date_posted",
        "from_date",
        "rooms",
        "adults",
        "paid",
    )

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        (
            "Booking Information",
            {
                "fields": (
                    "stay",
                    "from_date",
                    "to_date",
                    "passengers",
                    "type_of_room",
                    "rooms",
                    "adults",
                    "children",
                    "transport",
                )
            },
        ),
        ("Other Information", {"fields": ("message", "confirmation_code", "paid")}),
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "stay__name",
        "stay__property_name",
    )

    ordering = ("date_posted",)


class LodgePackageBookingAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "from_date",
        "to_date",
        "type_of_package",
        "paid",
    )

    list_filter = (
        "date_posted",
        "from_date",
        "paid",
    )

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        (
            "Booking Information",
            {
                "fields": (
                    "stay",
                    "from_date",
                    "to_date",
                    "type_of_package",
                )
            },
        ),
        ("Other Information", {"fields": ("message", "paid")}),
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "stay__name",
        "stay__property_name",
    )

    ordering = ("date_posted",)


class LodgePackageBookingInstallmentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "from_date",
        "to_date",
        "type_of_package",
        "paid_installment_1",
        "paid_installment_2",
        "paid_installment_3",
    )

    list_filter = (
        "date_posted",
        "from_date",
        "paid_installment_1",
        "paid_installment_2",
        "paid_installment_3",
    )

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        (
            "Booking Information",
            {
                "fields": (
                    "stay",
                    "from_date",
                    "to_date",
                    "type_of_package",
                )
            },
        ),
        (
            "Other Information",
            {
                "fields": (
                    "message",
                    "paid_installment_1",
                    "paid_installment_2",
                    "paid_installment_3",
                )
            },
        ),
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "stay__name",
        "stay__property_name",
    )

    ordering = ("date_posted",)


class EventTransportAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "passengers",
        "type_of_transport",
        "phone",
        "confirmation_code",
        "paid",
    )

    list_filter = (
        "passengers",
        "date_posted",
        "paid",
    )

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        (
            "Booking Information",
            {
                "fields": (
                    "passengers",
                    "type_of_transport",
                )
            },
        ),
        ("Other Information", {"fields": ("message", "confirmation_code", "paid")}),
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "type_of_transport",
    )

    ordering = ("date_posted",)


class StayAdmin(NestedModelAdmin):
    inlines = (
        ExtrasIncludedInline,
        FactsInline,
        InclusionsInline,
        StayImageInline,
        PrivateSafariAdmin,
        SharedSafariAdmin,
        AllInclusiveAdmin,
        OtherOptionAdmin,
    )
    raw_id_fields = ("user",)

    list_display = (
        "property_name",
        "name",
        "rooms",
        "bathrooms",
        "capacity",
        "is_active",
    )

    list_filter = (
        "date_posted",
        "date_updated",
        "is_an_event",
        "has_holiday_package",
        "is_active",
        "bathrooms",
        "rooms",
        "capacity",
    )

    fieldsets = (
        (
            None,
            {"fields": ("user", "type_of_stay", "room_type")},
        ),
        (
            "About",
            {
                "fields": (
                    "property_name",
                    "name",
                    "tags",
                    "rooms",
                    # "beds",
                    "bathrooms",
                    "capacity",
                    "description",
                    "unique_about_place",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "country",
                    "city",
                    "location",
                    "longitude",
                    "latitude",
                )
            },
        ),
        (
            "Amenities",
            {
                "fields": (
                    "swimming_pool",
                    "hot_tub",
                    "sauna",
                    "gym",
                    "patio",
                    "terrace",
                    "balcony",
                    "firepit",
                    "barbecue_grill",
                    "outdoor_dining_area",
                    "spa",
                    "wifi",
                    "parking",
                    "tv",
                    "air_conditioning",
                    "heating",
                    "kitchen",
                    "fridge",
                    "laundry",
                    "washing_machine",
                    "dedicated_working_area",
                    "smoke_alarm",
                    "first_aid_kit",
                    "medical_service_on_site",
                    "carbon_monoxide_detector",
                    "lockable_room",
                    "bar",
                    "restaurant",
                    "giftshop",
                    "photography_room",
                    "themed_room",
                    "pet_friendly",
                    "barber_shop",
                    "beauty_salon",
                    "purified_drinking_water",
                    "firewood",
                    "conference_center",
                    "ensuite_room",
                    "library",
                )
            },
        ),
        (
            "Best describes as",
            {
                "fields": (
                    "tented_camp",
                    "lodge",
                    "house",
                    "campsite",
                    "weekend_getaway",
                    "romantic_getaway",
                    "group_getaway",
                    "conservancy",
                    "farmstay",
                    "national_park_game_reserves",
                    "lakefront",
                    "beachfront",
                    "luxurious",
                    "beautiful_view",
                    "off_grid",
                    "eco_stay",
                    "quirky",
                    "honeymoon_spot",
                    "unique_experiences",
                    "traditional",
                    "mansion",
                    "over_water",
                    "stunning_architecture",
                    "riverfront",
                    "private_house",
                    "resort",
                    "boutique_hotel",
                    "unique_space",
                    "unique_location",
                    "hotel",
                    "cottage",
                    "coworking_spot",
                    "fast_wifi",
                    "locally_owned",
                    "community_owned",
                    "carbon_neutral",
                    "owner_operated",
                    "popular",
                    "wellness_retreat",
                )
            },
        ),
        (
            "Contact",
            {"fields": ("contact_name", "contact_email", "contact_phone", "company")},
        ),
        (
            "Standard pricing",
            {
                "fields": (
                    "standard",
                    "price_non_resident",
                    "price",
                )
            },
        ),
        (
            "Price Per House",
            {
                "fields": (
                    "per_house",
                    "per_house_price",
                )
            },
        ),
        (
            "Policies",
            {
                "fields": (
                    "cancellation_policy",
                    "cancellation_policy_by_provider",
                    "health_and_safety_policy",
                    "damage_policy_by_provider",
                )
            },
        ),
        (
            "Others",
            {
                "fields": (
                    "pricing_type",
                    "in_homepage",
                    "has_options",
                    "is_active",
                )
            },
        ),
        (
            "Transport",
            {
                "fields": (
                    "car_transfer_price",
                    "car_transfer_text_location",
                    "bus_transfer_price",
                    "bus_transfer_text_location",
                )
            },
        ),
        (
            "Event",
            {
                "fields": (
                    "is_an_event",
                    "has_holiday_package",
                    "distance_from_venue",
                    "has_min_date",
                    "date_starts_from_ninth",
                )
            },
        ),
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "name",
        "property_name",
    )

    ordering = ("date_posted", "date_updated")


admin.site.register(Stays, StayAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(LodgePackageBooking, LodgePackageBookingAdmin)
admin.site.register(LodgePackageBookingInstallment, LodgePackageBookingInstallmentAdmin)
admin.site.register(EventTransport, EventTransportAdmin)
# admin.site.register(StayImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(SaveStays)
