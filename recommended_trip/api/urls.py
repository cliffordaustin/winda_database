from unicodedata import name
from .views import *
from django.urls import path


urlpatterns = [
    path("recommended-trips/", TripListView.as_view(), name="recommended-trips"),
    path(
        "recommended-trips/<slug:slug>/",
        TripDetailView.as_view(),
        name="recommended-trips-detail",
    ),
    path(
        "request-custom-trip/",
        RequestCustomTripListCreatView.as_view(),
        name="request-custom-trip",
    ),
    path(
        "recommended-trips/<slug:slug>/request-info/",
        RequestInfoListCreatView.as_view(),
        name="request-info",
    ),
]
