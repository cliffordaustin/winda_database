from .views import *
from django.urls import path


urlpatterns = [
    path("curated-trips/", CuratedTripListView.as_view(), name="curated-trips"),
    path(
        "curated-trips/<slug:slug>/",
        CuratedTripDetailView.as_view(),
        name="curated-trips-detail",
    ),
    path(
        "curated-trips/<slug:slug>/request-info/",
        RequestInfoOnCustomTripListCreatView.as_view(),
        name="request-info",
    ),
    path(
        "curated-trips/<trip_slug>/create-booked-trip/",
        BookedTripCreateAPIView.as_view(),
        name="booked-curated-trip-create",
    ),
    path(
        "create-trip-wizard/", TripWizardCreateView.as_view(), name="create-trip-wizard"
    ),
    path(
        "curated-trips/<trip_slug>/locations/",
        LocationListView.as_view(),
        name="itinerary-locations",
    ),
]
