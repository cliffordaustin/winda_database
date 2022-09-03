from rest_framework import generics

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
from rest_framework.permissions import IsAuthenticated

# curated trip views
class CuratedTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CuratedTripSerializer
    lookup_field = "slug"

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

    ordering_fields = [
        "name",
        "created_at",
    ]

    def get_queryset(self):
        queryset = CuratedTrip.objects.filter(is_active=True)

        querystring = self.request.GET.get("location").split(",")[0]
        if querystring:
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(area_covered__icontains=word)
            queryset = CuratedTrip.objects.filter(query).filter(is_active=True)

        return queryset


# user trip views
class UserTripsListView(generics.ListAPIView):
    serializer_class = UserTripsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserTrips.objects.filter(user=self.request.user)


class UserTripsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTripsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = UserTrips.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = UserTrips.objects.filter(slug=slug)
        return queryset


class UserTripListView(generics.ListAPIView):
    serializer_class = UserTripSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserTrip.objects.filter(user=self.request.user)


class UserTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = UserTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = UserTrip.objects.filter(slug=slug)
        return queryset


class UserTripCreateView(generics.CreateAPIView):
    queryset = UserTrip.objects.all()
    serializer_class = UserTripSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("trip_slug")

        if trip_slug is not None:
            trips = generics.get_object_or_404(UserTrips, slug=trip_slug)
            serializer.save(user=self.request.user, trips=trips)

        else:
            trips = UserTrips.objects.create(user=self.request.user, paid=False)
            serializer.save(user=self.request.user, trips=trips)


class UserStayTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserStayTripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = UserStayTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = UserStayTrip.objects.filter(slug=slug)
        return queryset


class UserStayTripCreateView(generics.CreateAPIView):
    queryset = UserStayTrip.objects.all()
    serializer_class = UserStayTripSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("trip_slug")
        trip = generics.get_object_or_404(UserTrip, slug=trip_slug)
        serializer.save(trip=trip)


class UserActivityTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserActivityTripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = UserActivityTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = UserActivityTrip.objects.filter(slug=slug)
        return queryset


class UserActivityTripCreateView(generics.CreateAPIView):
    queryset = UserActivityTrip.objects.all()
    serializer_class = UserActivityTripSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("trip_slug")
        trip = generics.get_object_or_404(UserTrip, slug=trip_slug)
        serializer.save(trip=trip)


class UserTransportationTripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTransportationTripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = UserTransportTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = UserTransportTrip.objects.filter(slug=slug)
        return queryset


class UserTransportationTripCreateView(generics.CreateAPIView):
    queryset = UserTransportTrip.objects.all()
    serializer_class = UserTransportationTripSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("trip_slug")
        trip = generics.get_object_or_404(UserTrip, slug=trip_slug)
        serializer.save(trip=trip)
