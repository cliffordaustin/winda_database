from rest_framework import generics
from django.conf import settings

from curated_trip.api.filterset import RecommendedTripFilter
from .serializers import *
from curated_trip.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
import re
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from anymail.message import EmailMessage


# curated trip views
class CuratedTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CuratedTripSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CuratedTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = CuratedTrip.objects.filter(slug=slug)
        return queryset


class CuratedTripListView(generics.ListCreateAPIView):
    serializer_class = CuratedTripSerializer
    filterset_class = RecommendedTripFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]

    ordering_fields = [
        "name",
        "created_at",
    ]

    def get_queryset(self):
        queryset = CuratedTrip.objects.filter(is_active=True)

        querystring = self.request.GET.get("location")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                query |= Q(locations__location__icontains=word)
            queryset = (
                CuratedTrip.objects.filter(query).filter(is_active=True).distinct()
            )

        return queryset


class LocationListView(generics.ListAPIView):
    serializer_class = CuratedTripLocationsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        trip_slug = self.kwargs.get("trip_slug")
        trip = generics.get_object_or_404(CuratedTrip, slug=trip_slug)
        return trip.locations.all()


class BookedTripCreateAPIView(generics.CreateAPIView):
    queryset = BookedTrip.objects.all()
    serializer_class = BookedTripSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("trip_slug")
        trip = generics.get_object_or_404(CuratedTrip, slug=trip_slug)
        serializer.save(trip=trip)

        # message sent to the user
        booking_request = self.request.data["booking_request"]
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        if booking_request:
            message.template_id = "4342930"
        else:
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

        # message sent to the admin
        order_message = EmailMessage(
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        order_message.template_id = "4219329"
        order_message.from_email = None
        order_message.merge_data = {
            self.request.data["email"]: {
                "user_email": self.request.data["email"],
                "booking_type": "a curated trip",
                "name": trip.name,
            },
        }

        order_message.merge_global_data = {
            "user_email": self.request.data["email"],
            "booking_type": "a curated trip",
            "name": trip.name,
        }
        order_message.send(fail_silently=True)


class RequestInfoOnCustomTripListCreatView(generics.ListCreateAPIView):
    serializer_class = RequestInfoOnCustomTripSerializer
    queryset = RequestInfoOnCustomTrip.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("slug")
        custom_trip = CuratedTrip.objects.get(slug=trip_slug)

        serializer.save(custom_trip=custom_trip)


class EbookEmailCreateView(generics.CreateAPIView):
    serializer_class = EbookEmailSerializer
    queryset = EbookEmail.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if EbookEmail.objects.filter(email=self.request.data["email"]).exists():
            EbookEmail.objects.filter(email=self.request.data["email"]).update(
                email=self.request.data["email"]
            )
        else:
            serializer.save()


class TripWizardCreateView(generics.CreateAPIView):
    serializer_class = TripWizardSerializer
    queryset = TripWizard.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

        # message sent to the user
        message = EmailMessage(
            to=[self.request.data["email"]],
        )
        message.template_id = "4353127"
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
        order_message.template_id = "4353135"
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
