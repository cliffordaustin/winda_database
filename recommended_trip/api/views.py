from rest_framework import generics

from recommended_trip.api.filterset import RecommendedTripFilter
from .serializers import *
from recommended_trip.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    lookup_field = "slug"

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

    ordering_fields = [
        "name",
        "created_at",
    ]

    def get_queryset(self):
        queryset = SingleTrip.objects.all()
        return queryset
