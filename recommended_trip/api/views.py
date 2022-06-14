from rest_framework import generics
from .serializers import *
from recommended_trip.models import *


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

    def get_queryset(self):
        queryset = SingleTrip.objects.all()
        return queryset
