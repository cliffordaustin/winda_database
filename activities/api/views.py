import re
from activities.api.filterset import ActivitiesFilter
from .filterset import ReviewFilter
from lodging.api.pagination import Pagination
from .serializers import (
    ActivityImageSerializer,
    ActivitySerializer,
    ActivityViewsSerializer,
    CartSerializer,
    OrderSerializer,
    ReviewSerializer,
)
from activities.models import Activities, ActivitiesImage, Cart, Order, Review, Views
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsUserActivityInstance, ObjectPermission
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import F, Value, CharField, Q


class ActivityCreateView(generics.CreateAPIView):
    serializer_class = ActivitySerializer
    queryset = Activities.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Activities.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Activities.objects.filter(slug=slug)
        return queryset


class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    filterset_class = ActivitiesFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "price",
        "capacity",
    ]

    def get_queryset(self):
        queryset = Activities.objects.all()

        querystring = self.request.GET.get("search")
        if querystring:
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word)
            queryset = Activities.objects.filter(query).all()

        return queryset


class ActivityImageListView(generics.ListAPIView):
    serializer_class = ActivityImageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = ActivitiesImage.objects.all()

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(Activities, slug=activity_slug)
            queryset = ActivitiesImage.objects.filter(activity=activity)

        return queryset


class ActivityImageCreateView(generics.CreateAPIView):
    queryset = ActivitiesImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        activity_slug = self.kwargs.get("activity_slug")
        activity = generics.get_object_or_404(Activities, slug=activity_slug)
        activity_queryset = Activities.objects.filter(
            slug=activity_slug, user=self.request.user
        )

        if not activity_queryset.exists():
            raise PermissionDenied("You can't add an image to this activity.")
        return serializer.save(activity=activity)


class ActivityImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityImageSerializer
    permission_classes = [IsUserActivityInstance]

    def get_queryset(self):

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(ActivitiesImage, slug=activity_slug)
            queryset = ActivitiesImage.objects.filter(activity=activity)

            return queryset


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Review.objects.all()

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(Activities, slug=activity_slug)
            queryset = Review.objects.filter(activity=activity)

        return queryset


class CreateActivityViews(generics.CreateAPIView):
    serializer_class = ActivityViewsSerializer
    queryset = Views.objects.all()

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def perform_create(self, serializer):
        activity_slug = self.kwargs.get("activity_slug")
        activity = generics.get_object_or_404(Activities, slug=activity_slug)

        ip = self.get_user_ip(self.request)
        activity_queryset = Views.objects.filter(activity=activity, user_ip=ip)

        if activity_queryset.exists():
            return None
        return serializer.save(activity=activity, user_ip=ip)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        activity_slug = self.kwargs.get("activity_slug")
        activity = generics.get_object_or_404(Activities, slug=activity_slug)

        review_queryset = Review.objects.filter(
            user=self.request.user, activity=activity
        )

        activity_queryset = Activities.objects.filter(
            slug=activity_slug, user=self.request.user
        )

        if review_queryset.exists():
            raise ValidationError("User has already reviewed this listing")

        elif activity_queryset.exists():
            raise PermissionDenied("You can't make a review on your listing")

        serializer.save(activity=activity, user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ObjectPermission]

    def get_queryset(self):

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(Activities, slug=activity_slug)
            queryset = Review.objects.filter(activity=activity)

        return queryset


class CartItemAPIView(APIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, ObjectPermission]

    def post(self, request, activity_slug, pk=None):
        activity = generics.get_object_or_404(Activities, slug=activity_slug)
        cart = Cart.objects.create(user=request.user, activity=activity)
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
        activity_slug = self.kwargs.get("activity_slug")
        activity = generics.get_object_or_404(Activities, slug=activity_slug)

        serializer.save(user=self.request.user, activity=activity)


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
