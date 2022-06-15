from requests import delete
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


class GroupTripPaidView(generics.ListAPIView):
    serializer_class = GroupTripSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return GroupTrip.objects.filter(user=self.request.user, paid=False)


class TripView(APIView):
    serializer_class = GroupTripSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        group_trip = GroupTrip.objects.filter(user=self.request.user, paid=False)
        serializer = GroupTripSerializer(group_trip, many=True)
        return Response(serializer.data)

    def delete(self, request, slug):
        if slug is not None:
            group_trip = generics.get_object_or_404(GroupTrip, slug=slug)

            for trip in group_trip.trip.all():
                trip.delete()

            group_trip.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, slug):
        stay_id = request.data.get("stay_id", None)
        activity_id = request.data.get("activity_id", None)
        transport_id = request.data.get("transport_id", None)
        nights = request.data.get("nights", 3)
        from_date = request.data.get("from_date", timezone.now())
        activity_from_date = request.data.get("activity_from_date", timezone.now())
        transport_from_date = request.data.get("transport_from_date", timezone.now())
        user_need_a_driver = request.data.get("user_need_a_driver", False)
        number_of_people = request.data.get("number_of_people", 1)
        number_of_days = request.data.get("number_of_days", None)
        starting_point = request.data.get("starting_point", None)
        destination = request.data.get("destination", None)
        distance = request.data.get("distance", None)
        stay_num_of_adults = request.data.get("stay_num_of_adults", 1)
        stay_num_of_children = request.data.get("stay_num_of_children", 0)
        stay_plan = request.data.get("stay_plan", "STANDARD")
        stay_non_resident = request.data.get("stay_non_resident", False)
        activity_non_resident = request.data.get("activity_non_resident", False)
        activity_pricing_type = request.data.get("activity_pricing_type", "PER PERSON")
        activity_number_of_people = request.data.get("activity_number_of_people", 1)
        activity_number_of_sessions = request.data.get("activity_number_of_sessions", 1)
        activity_number_of_groups = request.data.get("activity_number_of_groups", 1)

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
            transport_from_date=transport_from_date,
            number_of_people=number_of_people,
            user_need_a_driver=user_need_a_driver,
            number_of_days=number_of_days,
            starting_point=starting_point,
            destination=destination,
            distance=distance,
            stay_num_of_adults=stay_num_of_adults,
            stay_num_of_children=stay_num_of_children,
            stay_plan=stay_plan,
            stay_non_resident=stay_non_resident,
            activity_non_resident=activity_non_resident,
            activity_pricing_type=activity_pricing_type,
            activity_number_of_people=activity_number_of_people,
            activity_number_of_sessions=activity_number_of_sessions,
            activity_number_of_groups=activity_number_of_groups,
        )

        if slug is not None:
            group_trip = generics.get_object_or_404(GroupTrip, slug=slug)

            group_trip.trip.add(trip)

            group_trip.save()

        else:
            group_trip = GroupTrip.objects.create(user=self.request.user, paid=False)

            group_trip.trip.add(trip)

            group_trip.save()

        all_trips = GroupTrip.objects.filter(user=self.request.user)
        serializer = GroupTripSerializer(all_trips, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
