from django.contrib import admin
from .models import Order, Stays, StayImage, Review, Cart


admin.site.register(Stays)
admin.site.register(StayImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
