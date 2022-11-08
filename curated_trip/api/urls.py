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
]
