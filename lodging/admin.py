from django.contrib import admin
from .models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class StayImageInline(admin.TabularInline):
    model = StayImage
    extra = 1


class ExtrasIncludedInline(admin.TabularInline):
    model = ExtrasIncluded
    extra = 1


class FactsInline(admin.TabularInline):
    model = Facts
    extra = 1


class InclusionsInline(admin.TabularInline):
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


# admin.site.register(TypeOfRooms, TypeOfRoomsAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "from_date",
        "to_date",
        "rooms",
        "adults",
        "children",
        "transport",
        "paid",
    )

    list_filter = ("date_posted", "from_date", "rooms", "adults", "children", "paid")

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
                    "rooms",
                    "adults",
                    "children",
                    "transport",
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


class StayAdmin(NestedModelAdmin):
    inlines = (
        ExtrasIncludedInline,
        FactsInline,
        InclusionsInline,
        StayImageInline,
        TypeOfRoomsAdmin,
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
                    # "standard_capacity",
                    "price_non_resident",
                    "single_price_non_resident",
                    "teen_price_non_resident",
                    "single_teen_price_non_resident",
                    "children_price_non_resident",
                    "single_child_price_non_resident",
                    "price",
                    "single_price",
                    "teen_price",
                    "single_teen_price",
                    "children_price",
                    "single_child_price",
                )
            },
        ),
        (
            "Deluxe pricing",
            {
                "fields": (
                    "deluxe",
                    # "deluxe_capacity",
                    "deluxe_price_non_resident",
                    "deluxe_single_price_non_resident",
                    "deluxe_teen_price_non_resident",
                    "deluxe_single_teen_price_non_resident",
                    "deluxe_children_price_non_resident",
                    "deluxe_single_child_price_non_resident",
                    "deluxe_price",
                    "deluxe_single_price",
                    "deluxe_teen_price",
                    "deluxe_single_teen_price",
                    "deluxe_children_price",
                    "deluxe_single_child_price",
                )
            },
        ),
        (
            "Family room pricing",
            {
                "fields": (
                    "family_room",
                    # "family_room_capacity",
                    "family_room_price_non_resident",
                    "family_room_single_price_non_resident",
                    "family_room_teen_price_non_resident",
                    "family_room_single_teen_price_non_resident",
                    "family_room_children_price_non_resident",
                    "family_room_single_child_price_non_resident",
                    "family_room_price",
                    "family_room_single_price",
                    "family_room_teen_price",
                    "family_room_single_teen_price",
                    "family_room_children_price",
                    "family_room_single_child_price",
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
            "Park or conservation pricing",
            {
                "fields": (
                    "conservation_or_park",
                    # "conservation_or_park_capacity",
                    "conservation_or_park_price_non_resident",
                    "conservation_or_park_single_price_non_resident",
                    "conservation_or_park_teen_price_non_resident",
                    "conservation_or_park_single_teen_price_non_resident",
                    "conservation_or_park_children_price_non_resident",
                    "conservation_or_park_single_child_price_non_resident",
                    "conservation_or_park_price",
                    "conservation_or_park_single_price",
                    "conservation_or_park_teen_price",
                    "conservation_or_park_single_teen_price",
                    "conservation_or_park_children_price",
                    "conservation_or_park_single_child_price",
                )
            },
        ),
        # (
        #     "Super deluxe pricing",
        #     {
        #         "fields": (
        #             "super_deluxe",
        #             "super_deluxe_capacity",
        #             "super_deluxe_price_non_resident",
        #             "super_deluxe_single_price_non_resident",
        #             "super_deluxe_price",
        #             "super_deluxe_single_price",
        #             "super_deluxe_children_price_non_resident",
        #             "super_deluxe_single_child_price_non_resident",
        #             "super_deluxe_children_price",
        #             "super_deluxe_single_child_price",
        #             "super_deluxe_teen_price_non_resident",
        #             "super_deluxe_single_teen_price_non_resident",
        #             "super_deluxe_teen_price",
        #             "super_deluxe_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Studio pricing",
        #     {
        #         "fields": (
        #             "studio",
        #             "studio_capacity",
        #             "studio_price_non_resident",
        #             "studio_single_price_non_resident",
        #             "studio_price",
        #             "studio_single_price",
        #             "studio_children_price_non_resident",
        #             "studio_single_child_price_non_resident",
        #             "studio_children_price",
        #             "studio_single_child_price",
        #             "studio_teen_price_non_resident",
        #             "studio_single_teen_price_non_resident",
        #             "studio_teen_price",
        #             "studio_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Double room pricing",
        #     {
        #         "fields": (
        #             "double_room",
        #             "double_room_capacity",
        #             "double_room_price_non_resident",
        #             "double_room_single_price_non_resident",
        #             "double_room_price",
        #             "double_room_single_price",
        #             "double_room_children_price_non_resident",
        #             "double_room_single_child_price_non_resident",
        #             "double_room_children_price",
        #             "double_room_single_child_price",
        #             "double_room_teen_price_non_resident",
        #             "double_room_single_teen_price_non_resident",
        #             "double_room_teen_price",
        #             "double_room_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Tripple room pricing",
        #     {
        #         "fields": (
        #             "tripple_room",
        #             "tripple_room_capacity",
        #             "tripple_room_price_non_resident",
        #             "tripple_room_single_price_non_resident",
        #             "tripple_room_price",
        #             "tripple_room_single_price",
        #             "tripple_room_children_price_non_resident",
        #             "tripple_room_single_child_price_non_resident",
        #             "tripple_room_children_price",
        #             "tripple_room_single_child_price",
        #             "tripple_room_teen_price_non_resident",
        #             "tripple_room_single_teen_price_non_resident",
        #             "tripple_room_teen_price",
        #             "tripple_room_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Quad room pricing",
        #     {
        #         "fields": (
        #             "quad_room",
        #             "quad_room_capacity",
        #             "quad_room_price_non_resident",
        #             "quad_room_single_price_non_resident",
        #             "quad_room_price",
        #             "quad_room_single_price",
        #             "quad_room_children_price_non_resident",
        #             "quad_room_single_child_price_non_resident",
        #             "quad_room_children_price",
        #             "quad_room_single_child_price",
        #             "quad_room_teen_price_non_resident",
        #             "quad_room_single_teen_price_non_resident",
        #             "quad_room_teen_price",
        #             "quad_room_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Queen room pricing",
        #     {
        #         "fields": (
        #             "queen_room",
        #             "queen_room_capacity",
        #             "queen_room_price_non_resident",
        #             "queen_room_single_price_non_resident",
        #             "queen_room_price",
        #             "queen_room_single_price",
        #             "queen_room_children_price_non_resident",
        #             "queen_room_single_child_price_non_resident",
        #             "queen_room_children_price",
        #             "queen_room_single_child_price",
        #             "queen_room_teen_price_non_resident",
        #             "queen_room_single_teen_price_non_resident",
        #             "queen_room_teen_price",
        #             "queen_room_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "King room pricing",
        #     {
        #         "fields": (
        #             "king_room",
        #             "king_room_capacity",
        #             "king_room_price_non_resident",
        #             "king_room_single_price_non_resident",
        #             "king_room_price",
        #             "king_room_single_price",
        #             "king_room_children_price_non_resident",
        #             "king_room_single_child_price_non_resident",
        #             "king_room_children_price",
        #             "king_room_single_child_price",
        #             "king_room_teen_price_non_resident",
        #             "king_room_single_teen_price_non_resident",
        #             "king_room_teen_price",
        #             "king_room_single_teen_price",
        #         )
        #     },
        # ),
        # (
        #     "Twin room pricing",
        #     {
        #         "fields": (
        #             "twin_room",
        #             "twin_room_capacity",
        #             "twin_room_price_non_resident",
        #             "twin_room_single_price_non_resident",
        #             "twin_room_price",
        #             "twin_room_single_price",
        #             "twin_room_children_price_non_resident",
        #             "twin_room_single_child_price_non_resident",
        #             "twin_room_children_price",
        #             "twin_room_single_child_price",
        #             "twin_room_teen_price_non_resident",
        #             "twin_room_single_teen_price_non_resident",
        #             "twin_room_teen_price",
        #             "twin_room_single_teen_price",
        #         )
        #     },
        # ),
        (
            "Presidential suite room pricing",
            {
                "fields": (
                    "presidential_suite_room",
                    # "presidential_suite_room_capacity",
                    "presidential_suite_room_price_non_resident",
                    "presidential_suite_room_single_price_non_resident",
                    "presidential_suite_room_teen_price_non_resident",
                    "presidential_suite_room_single_teen_price_non_resident",
                    "presidential_suite_room_children_price_non_resident",
                    "presidential_suite_room_single_child_price_non_resident",
                    "presidential_suite_room_price",
                    "presidential_suite_room_single_price",
                    "presidential_suite_room_teen_price",
                    "presidential_suite_room_single_teen_price",
                    "presidential_suite_room_children_price",
                    "presidential_suite_room_single_child_price",
                )
            },
        ),
        (
            "Emperor suite room pricing",
            {
                "fields": (
                    "emperor_suite_room",
                    # "emperor_suite_room_capacity",
                    "emperor_suite_room_price_non_resident",
                    "emperor_suite_room_single_price_non_resident",
                    "emperor_suite_room_teen_price_non_resident",
                    "emperor_suite_room_single_teen_price_non_resident",
                    "emperor_suite_room_children_price_non_resident",
                    "emperor_suite_room_single_child_price_non_resident",
                    "emperor_suite_room_price",
                    "emperor_suite_room_single_price",
                    "emperor_suite_room_teen_price",
                    "emperor_suite_room_single_teen_price",
                    "emperor_suite_room_children_price",
                    "emperor_suite_room_single_child_price",
                )
            },
        ),
        (
            "Executive suite room pricing",
            {
                "fields": (
                    "executive_suite_room",
                    # "executive_suite_room_capacity",
                    "executive_suite_room_price_non_resident",
                    "executive_suite_room_single_price_non_resident",
                    "executive_suite_room_teen_price_non_resident",
                    "executive_suite_room_single_teen_price_non_resident",
                    "executive_suite_room_children_price_non_resident",
                    "executive_suite_room_single_child_price_non_resident",
                    "executive_suite_room_price",
                    "executive_suite_room_single_price",
                    "executive_suite_room_teen_price",
                    "executive_suite_room_single_teen_price",
                    "executive_suite_room_children_price",
                    "executive_suite_room_single_child_price",
                )
            },
        ),
        (
            "Policies",
            {
                "fields": (
                    # "check_in_time",
                    # "check_out_time",
                    # "refundable",
                    # "refund_policy",
                    # "damage_policy",
                    # "children_allowed",
                    # "pets_allowed",
                    # "smoking_allowed",
                    # "events_allowed",
                    # "covid_19_compliance",
                    # "covid_19_compliance_details",
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
                    "is_active",
                )
            },
        ),
        ("Transport", {"fields": ("car_transfer_price", "bus_transfer_price")}),
        ("Event", {"fields": ("is_an_event",)}),
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
# admin.site.register(StayImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(SaveStays)
