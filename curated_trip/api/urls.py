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
        "curated-trips/<slug:slug>/date-pricing/",
        DateAndPricingListView.as_view(),
        name="date-pricing",
    ),
    path(
        "curated-trips/<slug:slug>/date-pricing/<slug:date_pricing_slug>/",
        DateAndPricingDetailView.as_view(),
        name="date-pricing-detail",
    ),
]
