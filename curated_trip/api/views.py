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
            words = re.split(r"[^A-Za-z']+", querystring)
            query = Q()  # empty Q object
            for word in words:
                # 'or' the queries together
                query |= Q(area_covered__icontains=word)
            queryset = CuratedTrip.objects.filter(query).filter(is_active=True)

        return queryset


# user trip views


class UserTripListView(generics.ListAPIView):
    serializer_class = UserTripSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserTrip.objects.filter(user=self.request.user, paid=False)


class TripView(APIView):
    serializer_class = UserTripSerializer
    permission_classes = (IsAuthenticated,)
