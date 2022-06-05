from .serializers import *
from trip.models import *
from lodging.models import *
from activities.models import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Trip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Trip.objects.filter(slug=slug)
        return queryset


class GroupTripUpdateView(generics.RetrieveUpdateAPIView):
    queryset = GroupTrip.objects.all()
    serializer_class = GroupTripSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = GroupTrip.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = GroupTrip.objects.filter(slug=slug)
        return queryset


class TripView(APIView):
    serializer_class = GroupTripSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        group_trip = GroupTrip.objects.filter(user=self.request.user, paid=False)
        serializer = GroupTripSerializer(group_trip, many=True)
        return Response(serializer.data)

    def post(self, request):
        stay_id = request.data.get("stay_id", None)
        activity_id = request.data.get("activity_id", None)
        transport_id = request.data.get("transport_id", None)
        nights = request.data.get("nights", 3)
        from_date = request.data.get("from_date", timezone.now())
        activity_from_date = request.data.get("activity_from_date", timezone.now())
        user_need_a_driver = request.data.get("user_need_a_driver", False)
        number_of_people = request.data.get("number_of_people", 1)
        is_transport_per_day = request.data.get("is_transport_per_day", False)

        stay = None
        activity = None
        transport = None

        if stay_id:
            stay = generics.get_object_or_404(Stays, pk=stay_id)

        if activity_id:
            activity = generics.get_object_or_404(Activities, pk=activity_id)

        if transport_id:
            transport = generics.get_object_or_404(Transportation, pk=transport_id)

        trip = Trip.objects.create(
            user=self.request.user,
            stay=stay,
            activity=activity,
            transport=transport,
            nights=nights,
            from_date=from_date,
            activity_from_date=activity_from_date,
            number_of_people=number_of_people,
            user_need_a_driver=user_need_a_driver,
            is_transport_per_day=is_transport_per_day,
        )

        group_trip = GroupTrip.objects.get_or_create(
            user=self.request.user, paid=False
        )[0]

        group_trip.trip.add(trip)

        group_trip.save()

        # serializer_context = {"request": request}
        # serializer = self.serializer_class(GroupTrip, context=serializer_context)

        all_trips = GroupTrip.objects.all()
        serializer = GroupTripSerializer(all_trips, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
