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
        return GroupTrip.objects.filter(
            user=self.request.user, paid=False
        )  # set paid to true


class TripView(APIView):
    serializer_class = GroupTripSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        group_trip = GroupTrip.objects.filter(user=self.request.user, paid=False)
        serializer = GroupTripSerializer(group_trip, many=True)
        return Response(serializer.data)

    def delete(self, request, slug=None):
        if slug is not None:
            group_trip = generics.get_object_or_404(GroupTrip, slug=slug)

            for trip in group_trip.trip.all():
                trip.delete()

            group_trip.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, slug=None):
        stay_id = request.data.get("stay_id", None)
        activity_id = request.data.get("activity_id", None)
        transport_id = request.data.get("transport_id", None)
        flight_id = request.data.get("flight_id", None)
        from_date = request.data.get("from_date", None)
        transport_number_of_days = request.data.get("transport_number_of_days", 1)
        activity_from_date = request.data.get("activity_from_date", None)
        transport_from_date = request.data.get("transport_from_date", None)
        user_need_a_driver = request.data.get("user_need_a_driver", False)
        starting_point = request.data.get("starting_point", None)
        destination = request.data.get("destination", None)
        distance = request.data.get("distance", None)
        stay_num_of_adults = request.data.get("stay_num_of_adults", 1)
        stay_num_of_children = request.data.get("stay_num_of_children", None)
        stay_num_of_adults_non_resident = request.data.get(
            "stay_num_of_adults_non_resident", None
        )
        stay_num_of_children_non_resident = request.data.get(
            "stay_num_of_children_non_resident", None
        )
        stay_plan = request.data.get("stay_plan", "STANDARD")
        activity_non_resident = request.data.get("activity_non_resident", False)
        activity_pricing_type = request.data.get("activity_pricing_type", "PER PERSON")
        activity_number_of_people = request.data.get("activity_number_of_people", 1)
        activity_number_of_people_non_resident = request.data.get(
            "activity_number_of_people_non_resident", None
        )
        activity_number_of_sessions = request.data.get(
            "activity_number_of_sessions", None
        )
        activity_number_of_sessions_non_resident = request.data.get(
            "activity_number_of_sessions_non_resident", None
        )
        activity_number_of_groups = request.data.get("activity_number_of_groups", None)
        activity_number_of_groups_non_resident = request.data.get(
            "activity_number_of_groups_non_resident", None
        )
        checked_for_availability = request.data.get("checked_for_availability", False)
        stay_is_not_available = request.data.get("stay_is_not_available", False)

        stay = None
        activity = None
        transport = None
        flight = None

        if stay_id:
            stay = generics.get_object_or_404(Stays, pk=stay_id)

        if activity_id:
            activity = generics.get_object_or_404(Activities, pk=activity_id)

        if transport_id:
            transport = generics.get_object_or_404(Transportation, pk=transport_id)

        if flight_id:
            flight = generics.get_object_or_404(Flight, pk=flight_id)

        trip = Trip.objects.create(
            user=self.request.user,
            stay=stay,
            activity=activity,
            transport=transport,
            flight=flight,
            from_date=from_date,
            transport_number_of_days=transport_number_of_days,
            activity_from_date=activity_from_date,
            transport_from_date=transport_from_date,
            user_need_a_driver=user_need_a_driver,
            starting_point=starting_point,
            destination=destination,
            distance=distance,
            stay_num_of_adults=stay_num_of_adults,
            stay_num_of_children=stay_num_of_children,
            stay_num_of_adults_non_resident=stay_num_of_adults_non_resident,
            stay_num_of_children_non_resident=stay_num_of_children_non_resident,
            stay_plan=stay_plan,
            activity_non_resident=activity_non_resident,
            activity_pricing_type=activity_pricing_type,
            activity_number_of_people=activity_number_of_people,
            activity_number_of_people_non_resident=activity_number_of_people_non_resident,
            activity_number_of_sessions=activity_number_of_sessions,
            activity_number_of_sessions_non_resident=activity_number_of_sessions_non_resident,
            activity_number_of_groups=activity_number_of_groups,
            activity_number_of_groups_non_resident=activity_number_of_groups_non_resident,
            checked_for_availability=checked_for_availability,
            stay_is_not_available=stay_is_not_available,
        )

        if slug is not None:
            group_trip = generics.get_object_or_404(GroupTrip, slug=slug)

            group_trip.trip.add(trip)

            group_trip.save()

        else:
            group_trip = GroupTrip.objects.create(user=self.request.user, paid=False)

            group_trip.trip.add(trip)

            group_trip.save()

        # all_trips = generics.get_object_or_404(GroupTrip, slug=group_trip.slug)
        # serializer = GroupTripSerializer(all_trips, many=True)
        # return Response(group_trip, status=status.HTTP_200_OK)

        serializer_context = {"request": request}
        serializer = self.serializer_class(group_trip, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
