from django.urls import path
from .views import *


urlpatterns = [
    path("stays/", StaysListView.as_view(), name="stays-list"),
    path("user-stays/", UserStays.as_view(), name="user-stays-list"),
    path("user-stays/<slug>/", UserStayDetailView.as_view(), name="user-stay"),
    path("events/", EventListView.as_view(), name="events-list"),
    path("all-stays/", AllStaysListView.as_view(), name="all-stays-list"),
    path("create-stay/", StaysCreateView.as_view(), name="stays-create"),
    path("stays/<slug>/", StaysDetailView.as_view(), name="stays-detail"),
    path(
        "stays/<stay_slug>/add-view/",
        CreateStayViews.as_view(),
        name="add_view_to_stay",
    ),
    path(
        "stays/<stay_slug>/create-event/",
        EventCreateView.as_view(),
        name="create_event_to_stay",
    ),
    path(
        "stays/<stay_slug>/create-lodge-package/",
        LodgePackageBookingCreateView.as_view(),
        name="create_lodge_package_stay",
    ),
    path(
        "stays/<stay_slug>/create-lodge-package-installment/",
        LodgePackageBookingInstallmentCreateView.as_view(),
        name="create_lodge_package_stay_installment",
    ),
    path(
        "event/create-transport/",
        EventTransportCreateView.as_view(),
        name="create_event_transport",
    ),
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
    path("stays/<stay_slug>/reviews/", ReviewListView.as_view(), name="reviews-list"),
    path(
        "stays/<stay_slug>/reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="reviews-detail",
    ),
    path(
        "stays/<stay_slug>/create-review/",
        ReviewCreateView.as_view(),
        name="reviews-create",
    ),
    path("stays/<stay_slug>/add-to-cart/", CartItemAPIView.as_view(), name="add-cart"),
    path(
        "user-cart/<int:pk>/",
        CartDetailView.as_view(),
        name="detail-cart-item",
    ),
    path("user-cart/", CartListView.as_view(), name="user-cart-items"),
    path("user-orders/", OrderListView.as_view(), name="orders-list"),
    path("user-orders/paid/", OrderPaidListView.as_view(), name="orders-paid-list"),
    path("user-orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "stays/<stay_slug>/add-to-order/",
        OrderCreateView.as_view(),
        name="order-create",
    ),
    path(
        "stays/<stay_slug>/save/",
        SaveStaysCreateView.as_view(),
        name="save-stay",
    ),
    path(
        "stays/<stay_id>/delete/",
        SaveStaysDeleteView.as_view(),
        name="delete-stay",
    ),
    path(
        "user-saved-stays/",
        SaveStaysListView.as_view(),
        name="user-saved-stays",
    ),
    path(
        "user-saved-stays/<int:pk>/",
        SaveStaysDetailView.as_view(),
        name="user-saved-stays-detail",
    ),
    path(
        "stays/<stay_slug>/add-room-type/",
        RoomTypeCreateView.as_view(),
        name="room-type-create",
    ),
    path(
        "stays/<stay_slug>/room-types/",
        RoomTypeListView.as_view(),
        name="room-type-list",
    ),
    path(
        "stays/<stay_slug>/room-types/<slug>/",
        RoomTypeDetailView.as_view(),
        name="room-type-detail",
    ),
    path(
        "room-types/<room_type_slug>/availabilities/",
        RoomAvailabilityListView.as_view(),
        name="room-availability-list",
    ),
    path(
        "room-types/<room_type_slug>/availabilities/<slug>/",
        RoomAvailabilityDetailView.as_view(),
        name="room-availability-detail",
    ),
    path(
        "room-types/<room_type_slug>/add-availability/",
        RoomAvailabilityCreateView.as_view(),
        name="room-availability-create",
    ),
    path(
        "room-types/<room_type_slug>/add-booking/",
        BookingsCreateView.as_view(),
        name="room-booking-create",
    ),
    path(
        "room-types/<room_type_slug>/bookings/",
        BookingsListView.as_view(),
        name="room-booking-list",
    ),
]
