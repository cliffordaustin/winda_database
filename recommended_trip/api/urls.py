from .views import *
from django.urls import path


urlpatterns = [
    path("recommended-trips/", TripListView.as_view(), name="recommended-trips"),
    path(
        "recommended-trips/<slug:slug>/",
        TripDetailView.as_view(),
        name="recommended-trips-detail",
    ),
]
