from django.contrib import admin
from .models import *


# class StayImageInline(admin.TabularInline):
#     model = StayImage
#     extra = 1


# class StayAdmin(admin.ModelAdmin):
#     inlines = (StayImageInline,)

#     fieldset = (
#         (
#             None,
#             {
#                 "fields": (
#                     "user",
#                     "type_of_stay",
#                     "price",
#                     "city",
#                     "country",
#                     "longitude",
#                     "latitude",
#                     "rooms",
#                     "beds",
#                     "bathrooms",
#                     "description",
#                     "unique_about_place",
#                     "pricing_type",
#                     "room_is_ensuite",
#                 )
#             }
#         )
#     )


admin.site.register(Stays)
admin.site.register(StayImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(SaveStays)
