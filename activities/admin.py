from django.contrib import admin
from .models import *


class EnquipmentProvidedInline(admin.TabularInline):
    model = EnquipmentProvided
    extra = 1


class EnquipmentRequiredByUserInline(admin.TabularInline):
    model = EnquipmentRequiredByUser
    extra = 1


class ActivitiesImageInline(admin.TabularInline):
    model = ActivitiesImage
    extra = 1


class FactsInline(admin.TabularInline):
    model = Facts
    extra = 1


class ActivitiesAdmin(admin.ModelAdmin):
    inlines = (
        EnquipmentProvidedInline,
        EnquipmentRequiredByUserInline,
        FactsInline,
        ActivitiesImageInline,
    )
    raw_id_fields = ("user",)

    list_display = (
        "user",
        "name",
        "city",
        "location",
    )

    list_filter = ("date_posted",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "name",
                )
            },
        ),
        (
            "About",
            {
                "fields": (
                    "tags",
                    "description",
                    "min_capacity",
                    "capacity",
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
            "Contact",
            {"fields": ("contact_name", "contact_email", "contact_phone", "company")},
        ),
        (
            "Price per person",
            {
                "fields": (
                    "price_per_person",
                    "price_non_resident",
                    "price",
                )
            },
        ),
        (
            "Price per session",
            {
                "fields": (
                    "price_per_session",
                    "session_price_non_resident",
                    "session_price",
                )
            },
        ),
        (
            "Price per group",
            {
                "fields": (
                    "price_per_group",
                    "group_price_non_resident",
                    "group_price",
                    "max_number_of_people_in_a_group",
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
    )


admin.site.register(Activities, ActivitiesAdmin)
# admin.site.register(ActivitiesImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(SaveActivities)
