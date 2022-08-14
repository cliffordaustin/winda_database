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

    class Meta:
        model = UserStayTrip
        exclude = ["trip"]


class UserActivityTripSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = UserActivityTrip
        exclude = ["trip"]


class UserTransportationTripSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = UserTransportTrip
        exclude = ["trip"]


class UserTripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_stay_trip = UserStayTripSerializer(read_only=True, many=True)
    user_activity_trip = UserActivityTripSerializer(read_only=True, many=True)
    user_transport_trip = UserTransportationTripSerializer(read_only=True, many=True)

    class Meta:
        model = UserTrip
        fields = "__all__"
