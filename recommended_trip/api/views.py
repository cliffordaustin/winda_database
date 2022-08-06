from rest_framework import generics

from recommended_trip.api.filterset import RecommendedTripFilter
from .serializers import *
from recommended_trip.models import *
from .pagination import TripPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
import re


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
    pagination_class = TripPagination

    ordering_fields = [
        "name",
        "created_at",
    ]

    def get_queryset(self):
        queryset = SingleTrip.objects.filter(is_active=True)

        querystring = self.request.GET.get("location")
        if querystring:
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= (
                    Q(area_covered__icontains=word)
                    | Q(stay__location__icontains=word)
                    | Q(stay__city__icontains=word)
                    | Q(activity__location__icontains=word)
                    | Q(activity__city__icontains=word)
                )
            queryset = SingleTrip.objects.filter(query).filter(is_active=True)

        return queryset
