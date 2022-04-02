from django.urls import path
from .views import (
    ActivityListView,
    ActivityCreateView,
    ActivityDetailView,
    ActivityImageCreateView,
    ActivityImageListView,
    ActivityImageDetailView,
)


urlpatterns = [
    path("activities/", ActivityListView.as_view(), name="activities-list"),
    path("create-activity/", ActivityCreateView.as_view(), name="activities-create"),
    path("activities/<slug>/", ActivityDetailView.as_view(), name="activities-detail"),
    path(
        "activities/<activity_slug>/images/",
        ActivityImageListView.as_view(),
        name="activity-images-list",
    ),
    path(
        "activities/<activity_slug>/create-image/",
        ActivityImageCreateView.as_view(),
        name="activity-images-create",
    ),
    path(
        "activities/<activity_slug>/images/<int:pk>/",
        ActivityImageDetailView.as_view(),
        name="activity-images-detail",
    ),
]
