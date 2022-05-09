import re
from lodging.api.pagination import Pagination
from .serializers import (
    CartSerializer,
    OrderSerializer,
    StayViewsSerializer,
    StaysSerializer,
    StayImageSerializer,
)
from lodging.models import Cart, Order, Stays, StayImage, Views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsUserStayInstance, ObjectPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filterset import StayFilter, ReviewFilter
from django.db.models import Q
from lodging.models import Review
from .serializers import ReviewSerializer
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.db.models import F, Value, CharField


class StaysCreateView(generics.CreateAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class StaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug)
        return queryset


class StaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "price",
        "rooms",
        "beds",
        "bathrooms",
    ]

    def get_queryset(self):
        queryset = Stays.objects.all()

        querystring = self.request.GET.get("search")
        if querystring:
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word)
            queryset = Stays.objects.filter(query).all()

        return queryset


class StayImageListView(generics.ListAPIView):
    serializer_class = StayImageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = StayImage.objects.all()

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

        return queryset


class StayImageCreateView(generics.CreateAPIView):
    queryset = StayImage.objects.all()
    serializer_class = StayImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        stay_queryset = Stays.objects.filter(slug=stay_slug, user=self.request.user)

        if not stay_queryset.exists():
            raise PermissionDenied("You can't add an image to this stay.")
        return serializer.save(stay=stay)


class StayImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StayImageSerializer
    permission_classes = [IsUserStayInstance]

    def get_queryset(self):

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

            return queryset


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Review.objects.all()

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = Review.objects.filter(stay=stay)

        return queryset


class CreateStayViews(generics.CreateAPIView):
    serializer_class = StayViewsSerializer
    queryset = Views.objects.all()

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        ip = self.get_user_ip(self.request)
        stay_queryset = Views.objects.filter(stay=stay, user_ip=ip)

        if stay_queryset.exists():
            return None
        return serializer.save(stay=stay, user_ip=ip)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        review_queryset = Review.objects.filter(user=self.request.user, stay=stay)

        stay_queryset = Stays.objects.filter(slug=stay_slug, user=self.request.user)

        if review_queryset.exists():
            raise ValidationError("User has already reviewed this listing")

        elif stay_queryset.exists():
            raise PermissionDenied("You can't make a review on your listing")

        serializer.save(stay=stay, user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ObjectPermission]

    def get_queryset(self):

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = Review.objects.filter(stay=stay)

        return queryset


class CartItemAPIView(APIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, ObjectPermission]

    def post(self, request, stay_slug, pk=None):
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        cart = Cart.objects.create(user=request.user, stay=stay)
        cart.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(cart, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(user=self.request.user, stay=stay)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=False)


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
