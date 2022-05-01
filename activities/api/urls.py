from django.urls import path
from .views import (
    ActivityListView,
    ActivityCreateView,
    ActivityDetailView,
    ActivityImageCreateView,
    ActivityImageListView,
    ActivityImageDetailView,
    CartDetailView,
    CartItemAPIView,
    CartListView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderPaidListView,
    ReviewCreateView,
    ReviewDetailView,
    ReviewListView,
    CreateActivityViews,
)


urlpatterns = [
    path("activities/", ActivityListView.as_view(), name="activities-list"),
    path("create-activity/", ActivityCreateView.as_view(), name="activities-create"),
    path("activities/<slug>/", ActivityDetailView.as_view(), name="activities-detail"),
    path(
        "activities/<slug>/add-view/",
        CreateActivityViews.as_view(),
        name="add-view-to-activities",
    ),
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
    path(
        "activities/<activity_slug>/reviews/",
        ReviewListView.as_view(),
        name="reviews-list",
    ),
    path(
        "activities/<activity_slug>/reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="reviews-detail",
    ),
    path(
        "activities/<activity_slug>/create-review/",
        ReviewCreateView.as_view(),
        name="reviews-create",
    ),
    path(
        "activities/<activity_slug>/add-to-cart/",
        CartItemAPIView.as_view(),
        name="add-cart",
    ),
    path(
        "user-activities-cart/<int:pk>/",
        CartDetailView.as_view(),
        name="detail-cart-item",
    ),
    path("user-activities-cart/", CartListView.as_view(), name="user-cart-items"),
    path("user-activities-orders/", OrderListView.as_view(), name="orders-list"),
    path(
        "user-activities-orders/paid/",
        OrderPaidListView.as_view(),
        name="orders-paid-list",
    ),
    path(
        "user-activities-orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "activities/<activity_slug>/add-to-order/",
        OrderCreateView.as_view(),
        name="order-create",
    ),
]
