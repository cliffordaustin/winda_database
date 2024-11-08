from rest_framework import serializers
from recommended_trip.models import *
from lodging.api.serializers import StaysSerializer
from activities.api.serializers import ActivitySerializer
from transport.api.serializers import (
    GeneralTransferSerializer,
    TransportSerializer,
    FlightSerializer,
)


class SingleTripImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleTripImage
        exclude = ["trip"]


class RecommendedMonthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedMonths
        exclude = ["trip"]


class TripHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripHighlight
        exclude = ["trip"]


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        exclude = ["trip"]


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        exclude = ["trip"]


class RequestCustomTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCustomTrip
        fields = "__all__"


class RequestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestInfo
        fields = "__all__"


class AvailableDatesInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDates
        exclude = ["trip"]


class TripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay = StaysSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    transport = TransportSerializer(read_only=True)
    flight = FlightSerializer(read_only=True)
    general_transfer = GeneralTransferSerializer(read_only=True)
    single_trip_images = SingleTripImageSerializer(many=True, read_only=True)
    trip_highlights = TripHighlightSerializer(many=True, read_only=True)
    itineraries = ItinerarySerializer(many=True, read_only=True)
    available_dates = AvailableDatesInlineSerializer(many=True, read_only=True)
    faqs = FrequentlyAskedQuestionSerializer(many=True, read_only=True)
    months = RecommendedMonthsSerializer(many=True, read_only=True)

    stay_id = serializers.PrimaryKeyRelatedField(
        queryset=Stays.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=Activities.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    general_transfer_id = serializers.PrimaryKeyRelatedField(
        queryset=GeneralTransfers.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = SingleTrip
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.transport = validated_data.get("transport_id", instance.transport)
        instance.flight = validated_data.get("flight_id", instance.flight)
        instance.general_transfer = validated_data.get(
            "general_transfer_id", instance.general_transfer
        )
        instance.activity = validated_data.get("activity_id", instance.activity)
        instance.stay = validated_data.get("stay_id", instance.stay)

        instance.save()
        return instance
