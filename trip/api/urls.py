from .views import *
from django.urls import path


urlpatterns = [
    path("trips/", TripView.as_view(), name="trip-list"),
    path("create-trip/", TripView.as_view(), name="trip-create"),
    path("trip/<slug>/", TripDetailView.as_view(), name="trip-detail"),
]
