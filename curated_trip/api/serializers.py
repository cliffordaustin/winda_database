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


class ItineraryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryLocation
        exclude = ["itinerary"]


class ItineraryTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryTransport
        exclude = ["itinerary"]


class IncludedItineraryActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = IncludedItineraryActivity
        exclude = ["itinerary"]


class OptionalItineraryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionalItineraryActivity
        exclude = ["itinerary"]


class ItineraryAccommodationSerializer(serializers.ModelSerializer):
    stay = StaysSerializer()

    class Meta:
        model = ItineraryAccommodation
        exclude = ["itinerary"]


class ItinerarySerializer(serializers.ModelSerializer):
    itinerary_locations = ItineraryLocationSerializer(many=True)
    itinerary_transports = ItineraryTransportSerializer(many=True)
    itinerary_activities = IncludedItineraryActivitySerializer(many=True)
    optional_activities = OptionalItineraryActivitySerializer(many=True)
    itinerary_accommodations = ItineraryAccommodationSerializer(many=True)

    class Meta:
        model = Itinerary
        exclude = ["trip"]


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        exclude = ["trip"]


class SimilarTripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarTrips
        fields = "__all__"


class CuratedTripLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuratedTripLocations
        exclude = ["curated_trip"]


class CuratedTripImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuratedTripImage
        exclude = ["trip"]


class CuratedTripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    curated_trip_images = CuratedTripImageSerializer(many=True)
    locations = CuratedTripLocationsSerializer(many=True)
    itineraries = ItinerarySerializer(many=True, read_only=True)
    similar_trips = SimilarTripsSerializer(many=True, read_only=True)
    faqs = FrequentlyAskedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = CuratedTrip
        fields = "__all__"
