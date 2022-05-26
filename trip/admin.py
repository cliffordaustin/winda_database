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

    list_filter = ("is_public",)
    search_fields = ("user__email",)
    ordering = ("updated_at",)


admin.site.register(Trip, TripAdmin)

admin.site.register(GroupTrip, GroupTripAdmin)
