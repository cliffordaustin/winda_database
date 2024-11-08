from rest_framework import generics

from recommended_trip.api.filterset import RecommendedTripFilter
from .serializers import *
from recommended_trip.models import *
from .pagination import TripPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
import re


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = SingleTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = SingleTrip.objects.filter(slug=slug)
        return queryset


class TripListView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    filterset_class = RecommendedTripFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = TripPagination
    permission_classes = [AllowAny]

    ordering_fields = [
        "name",
        "created_at",
    ]
    ordering = ["-area_covered", "price_non_resident"]

    def get_queryset(self):
        queryset = SingleTrip.objects.filter(is_active=True)

        querystring = self.request.GET.get("location")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                query |= Q(area_covered__icontains=word) | Q(
                    countries_covered__icontains=word
                )
            queryset = SingleTrip.objects.filter(
                query,
                is_active=True,
            ).all()

        return queryset


class AllTripsListView(generics.ListAPIView):
    serializer_class = TripSerializer
    filterset_class = RecommendedTripFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "name",
        "created_at",
    ]
    ordering = ["price_non_resident"]
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = SingleTrip.objects.filter(is_active=True)

        querystring = self.request.GET.get("location")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                query |= Q(area_covered__icontains=word) | Q(
                    countries_covered__icontains=word
                )
            queryset = SingleTrip.objects.filter(query).filter(is_active=True)

        return queryset


class RequestCustomTripListCreatView(generics.ListCreateAPIView):
    serializer_class = RequestCustomTripSerializer
    queryset = RequestCustomTrip.objects.all()
    permission_classes = [AllowAny]


class RequestInfoListCreatView(generics.ListCreateAPIView):
    serializer_class = RequestInfoSerializer
    queryset = RequestInfo.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("slug")
        trip = SingleTrip.objects.get(slug=trip_slug)

        serializer.save(trip=trip)
