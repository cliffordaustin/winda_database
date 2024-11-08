import re

from transport.api.filterset import ReviewFilter, TransportationFilter
from transport.api.pagination import Pagination, TransportPagination
from .serializers import *
from transport.models import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsUserTransportInstance, ObjectPermission


class FlightListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flight.objects.filter(
            paid=False,
            user_has_ordered=False,
            user=self.request.user,
            is_admin_entry=False,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightHasBeenOrderedView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flight.objects.filter(
            user_has_ordered=True, is_admin_entry=False, user=self.request.user
        )


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Flight.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Flight.objects.filter(slug=slug)
        return queryset


class GeneralTransfersListCreateView(generics.ListCreateAPIView):
    serializer_class = GeneralTransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeneralTransfers.objects.filter(
            paid=False,
            user_has_ordered=False,
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GeneralTransfersHasBeenOrderedView(generics.ListAPIView):
    serializer_class = GeneralTransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeneralTransfers.objects.filter(
            user_has_ordered=True, user=self.request.user
        )


class GeneralTransfersDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GeneralTransferSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = GeneralTransfers.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = GeneralTransfers.objects.filter(slug=slug)
        return queryset


class TransportCreateView(generics.CreateAPIView):
    serializer_class = TransportSerializer
    queryset = Transportation.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TransportListView(generics.ListAPIView):
    serializer_class = TransportSerializer
    filterset_class = TransportationFilter
    queryset = Transportation.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "price_per_day",
    ]
    pagination_class = TransportPagination

    def get_queryset(self):
        queryset = Transportation.objects.filter(is_active=True)

        querystring = self.request.GET.get("search")
        if querystring:
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(dropoff_city__icontains=word) | Q(
                    dropoff_country__icontains=word
                )
            queryset = Transportation.objects.filter(query, is_active=True).all()

        return queryset


class TransportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransportSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Transportation.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Transportation.objects.filter(slug=slug)
        return queryset


class TransportImageListView(generics.ListAPIView):
    serializer_class = TransportImagesSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = TransportationImage.objects.all()

        transport_slug = self.kwargs.get("transport_slug")
        if transport_slug is not None:
            transportation = generics.get_object_or_404(
                Transportation, slug=transport_slug
            )
            queryset = TransportationImage.objects.filter(transportation=transportation)

        return queryset


class TransportImageCreateView(generics.CreateAPIView):
    queryset = TransportationImage.objects.all()
    serializer_class = TransportImagesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transportation = generics.get_object_or_404(Transportation, slug=transport_slug)
        transport_queryset = Transportation.objects.filter(
            slug=transport_slug, user=self.request.user
        )

        if not transport_queryset.exists():
            raise PermissionDenied("You can't add an image to this transportation.")
        return serializer.save(transportation=transportation)


class TransportImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransportImagesSerializer
    permission_classes = [IsUserTransportInstance]

    def get_queryset(self):

        transport_slug = self.kwargs.get("transport_slug")
        if transport_slug is not None:
            transportation = generics.get_object_or_404(
                Transportation, slug=transport_slug
            )
            queryset = TransportationImage.objects.filter(transportation=transportation)

            return queryset


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Review.objects.all()

        transport_slug = self.kwargs.get("transport_slug")
        if transport_slug is not None:
            transport = generics.get_object_or_404(Transportation, slug=transport_slug)
            queryset = Review.objects.filter(transport=transport)

        return queryset


class CreateStayViews(generics.CreateAPIView):
    serializer_class = TransportViewsSerializer
    queryset = Views.objects.all()

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transport = generics.get_object_or_404(Transportation, slug=transport_slug)

        ip = self.get_user_ip(self.request)
        transport_queryset = Views.objects.filter(transport=transport, user_ip=ip)

        if transport_queryset.exists():
            return None
        return serializer.save(transport=transport, user_ip=ip)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transport = generics.get_object_or_404(Transportation, slug=transport_slug)

        review_queryset = Review.objects.filter(
            user=self.request.user, transport=transport
        )

        transport_queryset = Transportation.objects.filter(
            slug=transport_slug, user=self.request.user
        )

        if review_queryset.exists():
            raise ValidationError("User has already reviewed this listing")

        elif transport_queryset.exists():
            raise PermissionDenied("You can't make a review on your transport")

        serializer.save(transport=transport, user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ObjectPermission]

    def get_queryset(self):

        transport_slug = self.kwargs.get("transport_slug")
        if transport_slug is not None:
            transport = generics.get_object_or_404(Transportation, slug=transport_slug)
            queryset = Review.objects.filter(transport=transport)

        return queryset


class CartItemAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated, ObjectPermission]

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transport = generics.get_object_or_404(Transportation, slug=transport_slug)

        serializer.save(user=self.request.user, transport=transport)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transport = generics.get_object_or_404(Transportation, slug=transport_slug)

        serializer.save(user=self.request.user, transport=transport)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderPaidListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=True)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class SaveTransportCreateView(generics.CreateAPIView):
    serializer_class = SaveTransportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SaveTransportation.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        transport_slug = self.kwargs.get("transport_slug")
        transport = generics.get_object_or_404(Transportation, slug=transport_slug)

        save_queryset = SaveTransportation.objects.filter(
            user=self.request.user, transport=transport
        )

        if save_queryset.exists():
            raise ValidationError("User has already saved this transport")

        serializer.save(transport=transport, user=self.request.user)


class SaveTransportListView(generics.ListAPIView):
    serializer_class = SaveTransportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveTransportation.objects.filter(user=self.request.user)


class SaveTransportDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = SaveTransportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveTransportation.objects.filter(user=self.request.user)


class SaveTransportsDeleteView(generics.DestroyAPIView):
    serializer_class = SaveTransportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "transport_id"

    def get_queryset(self):
        return SaveTransportation.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        transport_id = self.kwargs.get("transport_id")
        transport = generics.get_object_or_404(Transportation, id=transport_id)

        save_queryset = SaveTransportation.objects.filter(
            user=self.request.user, transport=transport
        )

        if save_queryset.exists():
            save_queryset.delete()
