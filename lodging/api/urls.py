from django.urls import path
from .views import (
    StaysListView,
    StaysCreateView,
    StaysDetailView,
    StayImageCreateView,
    StayImageListView,
    StayImageDetailView,
)


urlpatterns = [
    path("stays/", StaysListView.as_view(), name="stays-list"),
    path("create-stay/", StaysCreateView.as_view(), name="stays-create"),
    path("stays/<slug>/", StaysDetailView.as_view(), name="stays-detail"),
    path(
        "stays/<stay_slug>/images/",
        StayImageListView.as_view(),
        name="stay-images-list",
    ),
    path(
        "stays/<stay_slug>/create-image/",
        StayImageCreateView.as_view(),
        name="stay-images-create",
    ),
    path(
        "stays/<stay_slug>/images/<int:pk>/",
        StayImageDetailView.as_view(),
        name="stay-images-detail",
    ),
]
