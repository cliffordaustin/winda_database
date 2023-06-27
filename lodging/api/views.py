import re
from lodging.api.pagination import Pagination, StayPagination, PartnerStayPagination
from .serializers import *
from lodging.models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from anymail.message import EmailMessage
from .permissions import IsUserStayInstance, ObjectPermission, IsUserRoomStayInstance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filterset import StayFilter, ReviewFilter, BookingsFilter
from django.db.models import Q
from lodging.models import Review
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.db.models import F, Value, CharField
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Prefetch

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)


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
        "rooms",
        "beds",
        "bathrooms",
    ]
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


# review
class UpdateStayView(APIView):
    def post(self, request):
        stay_id = request.data.get("stay_id")
        session_id = request.session
        print("Creating new session", session_id)
        user_id = request.user.id if request.user.is_authenticated else None

        if not stay_id:
            return Response(
                {"error": "Missing stay ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        stay = generics.get_object_or_404(Stays, id=stay_id)

        try:
            if user_id:
                # User is logged in
                stay.user_added_to_calculate.add(user_id)
            elif session_id:
                if session_id is None:
                    # Create a new session if it doesn't exist

                    request.session.create()
                    session_id = request.session.session_key
                # User is not logged in
                stay.annonymous_added_to_calculate.add(session_id)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"success": True})


class HighlightedStaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer

    def get_queryset(self):
        return Stays.objects.filter(in_homepage=True, has_options=True)


class HighlightedStaysDetailView(generics.RetrieveAPIView):
    serializer_class = StaysSerializer
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Stays.objects.filter(in_homepage=True, has_options=True, slug=slug)


class UserStays(generics.ListAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Stays.objects.filter(user=self.request.user)


class UserStaysEmail(generics.ListAPIView):
    serializer_class = LodgeStaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.user.email
        return (
            Stays.objects.filter(contact_email=email)
            .select_related("user")
            .prefetch_related(
                "stay_images",
            )
        )


class PartnerStaysDetailView(generics.ListAPIView):
    serializer_class = PartnerStaySerializer

    def get_queryset(self):
        list_ids = self.kwargs.get("list_ids")
        list_ids = list_ids.split(",")
        queryset = (
            Stays.objects.filter(is_partner_property=True, id__in=list_ids)
            .select_related("user")
            .prefetch_related(
                "activity_fees",
                "other_fees_resident",
                "other_fees_non_resident",
            )
        )

        return queryset


class PartnerStaysListView(generics.ListAPIView):
    serializer_class = LodgeStaySerializer

    def get_queryset(self):
        querystring = self.request.GET.get("search")

        query = Q()  # empty Q object

        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)

            for word in words:
                # 'or' the queries together
                query |= Q(location__icontains=word) | Q(city__icontains=word)

        else:
            queryset = (
                Stays.objects.filter(
                    query,
                    is_partner_property=True,
                )
                .select_related("user")
                .prefetch_related(
                    "stay_images",
                )
                .all()
            )

        return queryset


class UserStaysEmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.filter(
            user=self.request.user,
        )
        slug = self.kwargs.get("slug")
        email = self.request.user.email

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug, contact_email=email)
        return queryset


class RoomTypeCreateView(generics.CreateAPIView):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        serializer.save(stay=stay)


class RoomTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        if stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomType.objects.filter(stay=stay)

        return queryset


class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = queryset.filter(stay=stay)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(stay=stay).prefetch_related(
                Prefetch(
                    "room_resident_availabilities",
                    queryset=RoomAvailabilityResident.objects.filter(
                        date__range=[start_date, end_date]
                    ),
                ),
                Prefetch(
                    "room_non_resident_availabilities",
                    queryset=RoomAvailabilityNonResident.objects.filter(
                        date__range=[start_date, end_date]
                    ),
                ),
            )
        return queryset


class RoomAvailabilityListView(generics.ListAPIView):
    serializer_class = RoomAvailabilitySerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailability.objects.filter(room_type=room_type)

        return queryset


class OtherFeesResidentListView(generics.ListCreateAPIView):
    serializer_class = OtherFeesResidentSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesResident.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class ActivityFeesListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivityFeesSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ActivityFee.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class ActivityFeesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityFeesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(
            Stays, slug=stay_slug, is_partner_property=True
        )

        queryset = ActivityFee.objects.filter(stay=stay)

        return queryset


class OtherFeesNonResidentListView(generics.ListCreateAPIView):
    serializer_class = OtherFeesNonResidentSerializer

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesNonResident.objects.filter(stay=stay)

        return queryset

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        serializer.save(stay=stay)


class OtherFeesResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OtherFeesResidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesResident.objects.filter(stay=stay)

        return queryset


class OtherFeesNonResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OtherFeesNonResidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)

        queryset = OtherFeesNonResident.objects.filter(stay=stay)

        return queryset


class RoomAvailabilityResidentView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityResidentSerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        queryset = RoomAvailabilityResident.objects.filter(room_type=room_type)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = RoomAvailabilityResident.objects.filter(
                room_type=room_type,
                date__range=[start_date, end_date],
            ).order_by("date")

        return queryset

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        # check if date already exists then delete it
        for data in self.request.data:
            date = data["date"]
            RoomAvailabilityResident.objects.filter(
                room_type=room_type, date=date
            ).delete()

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_resident_guest_availabilities"]:
                RoomAvailabilityResidentGuest.objects.create(
                    room_availability_resident=availability, **item
                )

    def perform_update(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_resident_guest_availabilities"]:
                RoomAvailabilityResidentGuest.objects.update_or_create(
                    room_availability_resident=availability,
                    id=item["id"],
                    defaults=item,
                )


class RoomAvailabilityResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomAvailabilityResidentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityResident.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityNonResidentView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = RoomAvailabilityNonResidentSerializer

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityNonResident.objects.filter(room_type=room_type)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = RoomAvailabilityNonResident.objects.filter(
                room_type=room_type,
                date__range=[start_date, end_date],
            ).order_by("date")

        return queryset

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        # check if date already exists then delete it
        for data in self.request.data:
            date = data["date"]
            RoomAvailabilityNonResident.objects.filter(
                room_type=room_type, date=date
            ).delete()

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_non_resident_guest_availabilities"]:
                RoomAvailabilityNonResidentGuest.objects.create(
                    room_availability_non_resident=availability, **item
                )

    def perform_update(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        availabilities = serializer.save(room_type=room_type)

        for data, availability in zip(self.request.data, availabilities):
            for item in data["room_non_resident_guest_availabilities"]:
                RoomAvailabilityNonResidentGuest.objects.update_or_create(
                    room_availability_non_resident=availability,
                    id=item["id"],
                    defaults=item,
                )

    def allow_bulk_destroy(self, qs, filtered):
        return qs is not filtered


class RoomAvailabilityNonResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomAvailabilityNonResidentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")

        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        queryset = RoomAvailabilityNonResident.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        queryset = RoomAvailability.objects.filter(room_type=room_type)

        return queryset


class RoomAvailabilityResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = RoomType.objects.all()
    lookup_field = "slug"

    def perform_destroy(self, instance):
        room_type_slug = self.kwargs.get("slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        RoomAvailabilityResident.objects.filter(room_type=room_type).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomAvailabilityNonResidentDeleteView(generics.DestroyAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = RoomType.objects.all()
    lookup_field = "slug"

    def perform_destroy(self, instance):
        room_type_slug = self.kwargs.get("slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)
        RoomAvailabilityNonResident.objects.filter(room_type=room_type).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomAvailabilityCreateView(generics.CreateAPIView):
    serializer_class = RoomAvailabilitySerializer
    queryset = RoomAvailability.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        date = self.request.data.get("date")
        if date:
            RoomAvailability.objects.filter(room_type=room_type, date=date).delete()

        if room_type.stay.contact_email != self.request.user.email:
            raise PermissionDenied("You are not the owner of this stay")

        serializer.save(room_type=room_type)


class BookingsCreateView(generics.CreateAPIView):
    serializer_class = BookingsSerializer
    queryset = Bookings.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room_type_slug = self.kwargs.get("room_type_slug")
        room_type = generics.get_object_or_404(RoomType, slug=room_type_slug)

        serializer.save(room_type=room_type)


class BookingsListView(generics.ListAPIView):
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookingsFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        queryset = Bookings.objects.all()
        date = self.request.query_params.get("date")
        if date:
            queryset = Bookings.objects.filter(
                Q(check_in_date__lte=date) & Q(check_out_date__gte=date)
            )
        return queryset


class UserStayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [IsAuthenticated, IsUserStayInstance]
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
        "rooms",
        "beds",
        "bathrooms",
    ]
    ordering = []

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
        stay_queryset = Stays.objects.filter(
            slug=stay_slug, contact_email=self.request.user.email
        )

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


class RequestMail(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_partner:
            raise PermissionDenied

        elif request.method == "POST":
            message = EmailMessage(
                to=[settings.DEFAULT_FROM_EMAIL],
            )
            message.template_id = "4571457"
            message.from_email = None
            message.merge_data = {
                request.user.email: {
                    "name": request.user.first_name,
                    "user_email": request.user.email,
                },
            }

            message.merge_global_data = {
                "name": request.user.first_name,
                "user_email": request.user.email,
            }
            message.send(fail_silently=True)

            return Response({"message": "Mail sent successfully"})


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
