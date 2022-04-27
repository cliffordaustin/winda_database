from django.urls import path
from .views import (
    StaysListView,
    StaysCreateView,
    StaysDetailView,
    StayImageCreateView,
    StayImageListView,
    StayImageDetailView,
    ReviewCreateView,
    ReviewDetailView,
    ReviewListView,
    CreateStayViews,
    CartListView,
    CartDetailView,
    CartItemAPIView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
)


urlpatterns = [
    path("stays/", StaysListView.as_view(), name="stays-list"),
    path("create-stay/", StaysCreateView.as_view(), name="stays-create"),
    path("stays/<slug>/", StaysDetailView.as_view(), name="stays-detail"),
    path(
        "stays/<stay_slug>/add-view/",
        CreateStayViews.as_view(),
        name="add_view_to_stay",
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
    path("user-orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "stays/<stay_slug>/add-to-order/",
        OrderCreateView.as_view(),
        name="order-create",
    ),
]
