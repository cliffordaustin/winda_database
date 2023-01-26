import re
from lodging.api.pagination import Pagination, StayPagination
from .serializers import *
from lodging.models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from anymail.message import EmailMessage
from .permissions import IsUserStayInstance, ObjectPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filterset import StayFilter, ReviewFilter
from django.db.models import Q
from lodging.models import Review
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.db.models import F, Value, CharField
from django.conf import settings


class StaysCreateView(generics.CreateAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(
                slug=slug,
                is_active=True,
            )
        return queryset


class StaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        ("price", "price_non_resident"),
        "rooms",
        "beds",
        "bathrooms",
    ]
    ordering = ["price_non_resident"]
    pagination_class = StayPagination

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )

        querystring = self.request.GET.get("search")
        querystring_detail_search = self.request.GET.get("d_search")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word) | Q(city__icontains=word)
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        if querystring_detail_search:
            querystring_detail_search = querystring_detail_search.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring_detail_search)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= (
                    Q(location__icontains=word)
                    | Q(city__icontains=word)
                    | Q(country__icontains=word)
                )
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        return queryset


class UserStays(generics.ListAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Stays.objects.filter(user=self.request.user)


class UserStayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, user=self.request.user)
        return queryset


class EventListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        "rooms",
        "beds",
        "bathrooms",
    ]
    pagination_class = StayPagination

    def get_queryset(self):
        queryset = Stays.objects.filter(is_active=True, is_an_event=True)
        return queryset


class AllStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    filterset_class = StayFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "date_posted",
        ("price", "price_non_resident"),
        "rooms",
        "beds",
        "bathrooms",
    ]
    ordering = ["price_non_resident"]

    def get_queryset(self):
        queryset = Stays.objects.filter(
            is_active=True,
        )

        querystring = self.request.GET.get("search")
        querystring_detail_search = self.request.GET.get("d_search")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word) | Q(city__icontains=word)
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

        if querystring_detail_search:
            querystring_detail_search = querystring_detail_search.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring_detail_search)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= (
                    Q(location__icontains=word)
                    | Q(city__icontains=word)
                    | Q(country__icontains=word)
                )
            queryset = Stays.objects.filter(
                query,
                is_active=True,
            ).all()

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["date_posted", "rate"]
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


class CartItemAPIView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(user=self.request.user, stay=stay)


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

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4282998"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
                "stay_name": stay.name,
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
            "stay_name": stay.name,
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "an accommodation",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "an accommodation",
            "name": stay.name,
        }
        order_message.send(fail_silently=True)


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4282998"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "an accommodation",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "an accommodation",
            "name": stay.name,
        }

        order_message.send(fail_silently=True)


class LodgePackageBookingCreateView(generics.CreateAPIView):
    queryset = LodgePackageBooking.objects.all()
    serializer_class = LodgePackageBookingSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4491051"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "a lodge",
                "name": stay.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "a lodge",
            "name": stay.name,
        }

        order_message.send(fail_silently=True)


class LodgePackageBookingInstallmentCreateView(generics.CreateAPIView):
    queryset = LodgePackageBookingInstallment.objects.all()
    serializer_class = LodgePackageBookingInstallmentSerializer

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class EventTransportCreateView(generics.CreateAPIView):
    queryset = EventTransport.objects.all()
    serializer_class = EventTransportSerializer

    def perform_create(self, serializer):
        serializer.save()

        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4208873"
        message.from_email = None
        message.merge_data = {
            self.request.data["email"]: {
                "name": self.request.data["first_name"],
            },
        }

        message.merge_global_data = {
            "name": self.request.data["first_name"],
        }
        message.send(fail_silently=True)

        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
        }

        order_message.send(fail_silently=True)


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


class SaveStaysCreateView(generics.CreateAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        save_queryset = SaveStays.objects.filter(user=self.request.user, stay=stay)

        if save_queryset.exists():
            raise ValidationError("User has already saved this listing")

        serializer.save(stay=stay, user=self.request.user)


class SaveStaysListView(generics.ListAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)


class SaveStaysDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)


class SaveStaysDeleteView(generics.DestroyAPIView):
    serializer_class = SaveStaysSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "stay_id"

    def get_queryset(self):
        return SaveStays.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        stay_id = self.kwargs.get("stay_id")
        stay = generics.get_object_or_404(Stays, id=stay_id)

        save_queryset = SaveStays.objects.filter(user=self.request.user, stay=stay)

        if save_queryset.exists():
            save_queryset.delete()
