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

        querystring = self.request.GET.get("location")
        if querystring:
            querystring = querystring.split(",")[0]
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                query |= Q(area_covered__icontains=word)
            queryset = CuratedTrip.objects.filter(query).filter(is_active=True)

        return queryset


class RequestInfoOnCustomTripListCreatView(generics.ListCreateAPIView):
    serializer_class = RequestInfoOnCustomTripSerializer
    queryset = RequestInfoOnCustomTrip.objects.all()

    def perform_create(self, serializer):
        trip_slug = self.kwargs.get("slug")
        custom_trip = CuratedTrip.objects.get(slug=trip_slug)

        serializer.save(custom_trip=custom_trip)


class DateAndPricingListView(generics.ListAPIView):
    serializer_class = DateAndPricingSerializer

    def get_queryset(self):
        trip_slug = self.kwargs.get("slug")
        custom_trip = CuratedTrip.objects.get(slug=trip_slug)
        queryset = DateAndPricing.objects.filter(trip=custom_trip)
        return queryset


class DateAndPricingDetailView(generics.RetrieveAPIView):
    serializer_class = DateAndPricingSerializer

    def get_object(self):
        trip_slug = self.kwargs.get("slug")
        date_pricing_slug = self.kwargs.get("date_pricing_slug")
        date_pricing = generics.get_object_or_404(
            DateAndPricing,
            slug=date_pricing_slug,
            trip__slug=trip_slug,
        )
        return date_pricing
