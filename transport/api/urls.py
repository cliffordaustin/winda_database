from .views import *
from django.urls import path


urlpatterns = [
    path("transport/", TransportListView.as_view(), name="transport-list"),
    path("transport/<slug>/", TransportDetailView.as_view(), name="transport-detail"),
    path("transport/create/", TransportCreateView.as_view(), name="transport-create"),
    path(
        "transport/<transport_slug>/create-image/",
        TransportImageCreateView.as_view(),
        name="transport-image-create",
    ),
    path(
        "flights/",
        FlightListCreateView.as_view(),
        name="flight-list-create",
    ),
    path(
        "flights/<slug>/",
        FlightDetailView.as_view(),
        name="flight-detail",
    ),
    path(
        "general-transfers/",
        GeneralTransfersListCreateView.as_view(),
        name="general-transfer-list-create",
    ),
    path(
        "general-transfers/<slug>/",
        GeneralTransfersDetailView.as_view(),
        name="general-transfer-detail",
    ),
    path(
        "user-general-transfers-orders/",
        GeneralTransfersHasBeenOrderedView.as_view(),
        name="general-transfer-orders-list",
    ),
    path(
        "transport/<transport_slug>/images/",
        TransportImageListView.as_view(),
        name="transport-image-list",
    ),
    path(
        "transport/<transport_slug>/images/<int:pk>/",
        TransportImageDetailView.as_view(),
        name="transport-image-detail",
    ),
    path(
        "transport/<transport_slug>/reviews/",
        ReviewListView.as_view(),
        name="reviews-list",
    ),
    path(
        "transport/<transport_slug>/reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="reviews-detail",
    ),
    path(
        "transport/<transport_slug>/create-review/",
        ReviewCreateView.as_view(),
        name="reviews-create",
    ),
    path(
        "transport/<transport_slug>/add-to-cart/",
        CartItemAPIView.as_view(),
        name="add-cart",
    ),
    path("user-transport-cart/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    path("user-transport-cart/", CartListView.as_view(), name="cart-list"),
    path("user-transport-orders/", OrderListView.as_view(), name="orders-list"),
    path(
        "user-flight-orders/",
        FlightHasBeenOrderedView.as_view(),
        name="flight-orders-list",
    ),
    path(
        "user-transport-orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="orders-detail",
    ),
    path(
        "transport/<transport_slug>/add-to-order/",
        OrderCreateView.as_view(),
        name="orders-create",
    ),
    path(
        "user-transport-orders/paid/", OrderPaidListView.as_view(), name="orders-paid"
    ),
    path(
        "transport/<transport_slug>/save/",
        SaveTransportCreateView.as_view(),
        name="save-transport",
    ),
    path(
        "transport/<transport_id>/delete/",
        SaveTransportsDeleteView.as_view(),
        name="delete-transport",
    ),
    path(
        "user-saved-transports/",
        SaveTransportListView.as_view(),
        name="user-saved-transports",
    ),
    path(
        "user-saved-transports/<int:pk>/",
        SaveTransportDetailView.as_view(),
        name="user-saved-transports-detail",
    ),
]
