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
    search_fields = ("user__email",)
    ordering = ("updated_at",)
    list_display = ("user", "trip", "starting_date", "guests", "created_at")


admin.site.register(BookedTrip, BookedTripAdmin)

admin.site.register(Trip, TripAdmin)

admin.site.register(GroupTrip, GroupTripAdmin)
