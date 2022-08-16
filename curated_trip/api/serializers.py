from rest_framework import serializers
from curated_trip.models import *
from lodging.api.serializers import StaysSerializer
from activities.api.serializers import ActivitySerializer
from transport.api.serializers import TransportSerializer

# curated trip serializers
class CuratedTripImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuratedTripImage
        exclude = ["trip"]


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        exclude = ["trip"]


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        exclude = ["trip"]


class StayTripSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)

    class Meta:
        model = StayTrip
        exclude = ["trip"]


class ActivityTripSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = ActivityTrip
        exclude = ["trip"]


class TransportationTripSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = TransportationTrip
        exclude = ["trip"]


class CuratedTripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_trip = StayTripSerializer(read_only=True, many=True)
    activity_trip = ActivityTripSerializer(read_only=True, many=True)
    transport_trip = TransportationTripSerializer(read_only=True, many=True)
    curated_trip_images = CuratedTripImageSerializer(many=True, read_only=True)
    itineraries = ItinerarySerializer(many=True, read_only=True)
    faqs = FrequentlyAskedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = CuratedTrip
        fields = "__all__"


# user trip serializers
class UserStayTripSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)

    stay_id = serializers.PrimaryKeyRelatedField(
        queryset=Stays.objects.all(),
        write_only=True,
        required=True,
        allow_null=True,
    )

    def update(self, instance, validated_data):
        instance.stay = validated_data.get("stay_id", instance.stay)
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.to_date = validated_data.get("to_date", instance.to_date)
        instance.plan = validated_data.get("plan", instance.plan)
        instance.num_of_adults = validated_data.get(
            "num_of_adults", instance.num_of_adults
        )
        instance.num_of_children = validated_data.get(
            "num_of_children", instance.num_of_children
        )
        instance.num_of_adults_non_resident = validated_data.get(
            "num_of_adults_non_resident", instance.num_of_adults_non_resident
        )
        instance.num_of_children_non_resident = validated_data.get(
            "num_of_children_non_resident",
            instance.num_of_children_non_resident,
        )
        instance.save()
        return instance

    def create(self, validated_data):
        stay = validated_data.pop("stay_id")
        return UserStayTrip.objects.create(stay=stay, **validated_data)

    class Meta:
        model = UserStayTrip
        exclude = ["trip"]


class UserActivityTripSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)

    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=Activities.objects.all(),
        write_only=True,
        required=True,
        allow_null=True,
    )

    def update(self, instance, validated_data):
        instance.activity = validated_data.get("activity_id", instance.activity)
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.pricing_type = validated_data.get(
            "pricing_type", instance.pricing_type
        )
        instance.number_of_people = validated_data.get(
            "number_of_people", instance.number_of_people
        )
        instance.number_of_people_non_resident = validated_data.get(
            "number_of_people_non_resident", instance.number_of_people_non_resident
        )
        instance.number_of_sessions = validated_data.get(
            "number_of_sessions", instance.number_of_sessions
        )
        instance.number_of_sessions_non_resident = validated_data.get(
            "number_of_sessions_non_resident", instance.number_of_sessions_non_resident
        )
        instance.number_of_groups = validated_data.get(
            "number_of_groups", instance.number_of_groups
        )
        instance.number_of_groups_non_resident = validated_data.get(
            "number_of_groups_non_resident", instance.number_of_groups_non_resident
        )

        instance.save()
        return instance

    def create(self, validated_data):
        activity = validated_data.pop("activity_id")
        return UserActivityTrip.objects.create(activity=activity, **validated_data)

    class Meta:
        model = UserActivityTrip
        exclude = ["trip"]


class UserTransportationTripSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(),
        write_only=True,
        required=True,
        allow_null=True,
    )

    def update(self, instance, validated_data):
        instance.transport = validated_data.get("transport_id", instance.transport)
        instance.starting_point = validated_data.get(
            "starting_point", instance.starting_point
        )
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.number_of_days = validated_data.get(
            "number_of_days", instance.number_of_days
        )
        instance.user_need_a_driver = validated_data.get(
            "user_need_a_driver", instance.user_need_a_driver
        )

        instance.save()
        return instance

    def create(self, validated_data):
        transport = validated_data.pop("transport_id")
        return UserTransportTrip.objects.create(transport=transport, **validated_data)

    class Meta:
        model = UserTransportTrip
        exclude = ["trip"]


class UserTripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_stay_trip = UserStayTripSerializer(many=True)
    user_activity_trip = UserActivityTripSerializer(many=True)
    user_transport_trip = UserTransportationTripSerializer(many=True)

    class Meta:
        model = UserTrip
        exclude = ["trips"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    def create(self, validated_data):
        user_stay_trip = validated_data.pop("user_stay_trip")
        user_activity_trip = validated_data.pop("user_activity_trip")
        user_transport_trip = validated_data.pop("user_transport_trip")

        instance = UserTrip.objects.create(**validated_data)

        for stay in user_stay_trip:
            stay_queryset = stay["stay_id"]
            stay.pop("stay_id")
            UserStayTrip.objects.create(trip=instance, stay=stay_queryset, **stay)

        for activity in user_activity_trip:
            activity_queryset = activity["activity_id"]
            activity.pop("activity_id")
            UserActivityTrip.objects.create(
                trip=instance, activity=activity_queryset, **activity
            )

        for transport in user_transport_trip:
            transport_queryset = transport["transport_id"]
            transport.pop("transport_id")
            UserTransportTrip.objects.create(
                trip=instance, transport=transport_queryset, **transport
            )

        return instance


class UserTripsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    trip = UserTripSerializer(many=True)

    class Meta:
        model = UserTrips
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance
