from .views import *
from django.urls import path


urlpatterns = [
    path("trips/", TripView.as_view(), name="trip-list"),
    path("paid-trips/", GroupTripPaidView.as_view(), name="paid-trip-list"),
    path("trips/<slug>/", GroupTripUpdateView.as_view(), name="trip-detail"),
    path("create-trip/", TripView.as_view(), name="trip-create"),
    path("trips/<slug>/create-trip/", TripView.as_view(), name="trip-create"),
    path("trips/<slug>/delete-trip/", TripView.as_view(), name="trip-delete"),
    path("trip/<slug>/", TripDetailView.as_view(), name="trip-detail"),
    path("booked-trips/", BookedTripListAPIView.as_view(), name="booked-trip-list"),
    path(
        "booked-trips/<slug>/",
        BookedTripDetailAPIView.as_view(),
        name="booked-trip-detail",
    ),
    path(
        "trip/<trip_slug>/create-booked-trip/",
        BookedTripCreateAPIView.as_view(),
        name="booked-trip-create",
    ),
]
