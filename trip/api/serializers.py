from rest_framework import serializers
from trip.models import *


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class GroupTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTrip
        fields = "__all__"
        depth = 1
